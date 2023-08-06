// SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

#pragma once
#include <concepts>
#include <iosfwd>

#include <dune/common/classname.hh>
#include <dune/fufem/boundarypatch.hh>
#include <dune/geometry/quadraturerules.hh>
#include <dune/geometry/type.hh>
#include <dune/localfefunctions/cachedlocalBasis/cachedlocalBasis.hh>
#include <dune/localfefunctions/impl/standardLocalFunction.hh>
#include <dune/localfefunctions/manifolds/realTuple.hh>

#include <autodiff/forward/dual.hpp>
#include <autodiff/forward/dual/eigen.hpp>

#include <pyikarus/finiteElements/feBases/autodiffFE.hh>
#include <pyikarus/finiteElements/feBases/powerBasisFE.hh>
#include <pyikarus/finiteElements/feRequirements.hh>
#include <pyikarus/finiteElements/feTraits.hh>
#include <pyikarus/finiteElements/mechanics/materials.hh>
#include <pyikarus/finiteElements/physicsHelper.hh>
#include <pyikarus/utils/eigenDuneTransformations.hh>
#include <pyikarus/utils/linearAlgebraHelper.hh>
#include <pyikarus/utils/defaultFunctions.hh>

namespace Ikarus {

  template <typename Basis, typename Material_, typename FErequirements_ = FErequirements<>, bool useEigenRef = false>
  class NonLinearElastic : public PowerBasisFE<Basis>,
                                public Ikarus::AutoDiffFE<NonLinearElastic<Basis, Material_,FErequirements_,useEigenRef>, Basis,FErequirements_,useEigenRef> {
  public:
    using BaseDisp = PowerBasisFE<Basis>;  // Handles globalIndices function
    using BaseAD   = Ikarus::AutoDiffFE<NonLinearElastic<Basis, Material_,FErequirements_,useEigenRef>, Basis,FErequirements_,useEigenRef>;
    using BaseAD::size;
    using GlobalIndex = typename PowerBasisFE<Basis>::GlobalIndex;
    friend BaseAD;
    using FERequirementType = FErequirements_;
    using LocalView         = typename Basis::LocalView;
    using Element                = typename LocalView::Element;
    using Geometry          = typename Element::Geometry;
    using GridView          = typename Basis::GridView;
    using Material          = Material_;
    using GlobalBasis = Basis;

    template <typename VolumeLoad = LoadDefault, typename NeumannBoundaryLoad = LoadDefault>
    NonLinearElastic(const Basis& globalBasis, const typename LocalView::Element& element, const Material& p_mat,
                     VolumeLoad p_volumeLoad = {}, const BoundaryPatch<GridView>* neumannBoundary = nullptr,
                     NeumannBoundaryLoad p_neumannBoundaryLoad = {})
        : BaseDisp(globalBasis, element),
          BaseAD(globalBasis, element),
          localView_{globalBasis.localView()},
          neumannBoundary_{neumannBoundary},
          mat{p_mat} {
      localView_.bind(element);
      const int order = 2 * (localView_.tree().child(0).finiteElement().localBasis().order());
      localBasis      = Dune::CachedLocalBasis(localView_.tree().child(0).finiteElement().localBasis());
      localBasis.bind(Dune::QuadratureRules<double, Traits::mydim>::rule(localView_.element().type(), order),
                      Dune::bindDerivatives(0, 1));

      if constexpr (!std::is_same_v<VolumeLoad,LoadDefault>)
        volumeLoad =p_volumeLoad;
      if constexpr (!std::is_same_v<NeumannBoundaryLoad,LoadDefault>)
        neumannBoundaryLoad =p_neumannBoundaryLoad;

      assert(((not neumannBoundary_ and not neumannBoundaryLoad) or (neumannBoundary_ and neumannBoundaryLoad))
             && "If you pass a Neumann boundary you should also pass the function for the Neumann load!");
    }

    using Traits = TraitsFromLocalView<LocalView,useEigenRef>;
    const auto& localView() const { return localView_; }
  private:
    template <class ScalarType>
    ScalarType calculateScalarImpl(const FERequirementType& req, Eigen::VectorX<ScalarType>& dx) const {
      const auto& d      = req.getGlobalSolution(Ikarus::FESolutions::displacement);
      const auto& lambda = req.getParameter(Ikarus::FEParameter::loadfactor);
//      std::cout<<"Lambda: "<<lambda<<std::endl;
//      std::cout<<"d: "<<d.transpose()<<std::endl;
      using namespace Dune::DerivativeDirections;
      using namespace Dune;
      auto& first_child = localView_.tree().child(0);
      const auto& fe    = first_child.finiteElement();
      Dune::BlockVector<RealTuple<ScalarType, Traits::dimension>> disp(fe.size());

      for (auto i = 0U; i < fe.size(); ++i)
        for (auto k2 = 0U; k2 < Traits::mydim; ++k2)
          disp[i][k2] = dx[i * 2 + k2] + d[localView_.index(localView_.tree().child(k2).localIndex(i))[0]];

      ScalarType energy = 0.0;

      decltype(auto) matAD = mat.template rebind<ScalarType>();

      const auto geo = localView_.element().geometry();
      Dune::StandardLocalFunction uFunction(localBasis, disp, std::make_shared<const Geometry>(geo));
      for (const auto& [gpIndex, gp] : uFunction.viewOverIntegrationPoints()) {
        const auto u        = uFunction.evaluate(gpIndex);
        const auto H        = uFunction.evaluateDerivative(gpIndex, Dune::wrt(spatialAll), Dune::on(gridElement));
        const auto E        = (0.5 * (H.transpose() + H + H.transpose() * H)).eval();
        const auto EVoigt   = toVoigt(E);
        auto internalEnergy = matAD.template storedEnergy<StrainTags::greenLagrangian>(EVoigt);
        energy += internalEnergy * geo.integrationElement(gp.position()) * gp.weight();
      }
      // External forces volume forces over the domain
      if (volumeLoad) {
        for (const auto& [gpIndex, gp] : uFunction.viewOverIntegrationPoints()) {
          const auto uVal                              = uFunction.evaluate(gpIndex);
          Eigen::Vector<double, Traits::worlddim> fext = (*volumeLoad)(toEigen(gp.position()), lambda);
          energy -= uVal.dot(fext) * geo.integrationElement(gp.position()) * gp.weight();
        }
      }
      const int order = 2 * (localView_.tree().child(0).finiteElement().localBasis().order());
      // line or surface loads, i.e. neumann boundary
      if (not neumannBoundary_ and not neumannBoundaryLoad) return energy;
//      std::cout<<"if (not neumannBoundary_ and not neumannBoundaryLoad) return energy;"<<std::endl;
      auto element = localView_.element();
      for (auto&& intersection : intersections(neumannBoundary_->gridView(), element)) {
        if (not neumannBoundary_ or not neumannBoundary_->contains(intersection)) continue;

        const auto& quadLine = Dune::QuadratureRules<double, Traits::mydim - 1>::rule(intersection.type(), order);

        for (const auto& curQuad : quadLine) {
          // Local position of the quadrature point
          const Dune::FieldVector<double, Traits::mydim>& quadPos
              = intersection.geometryInInside().global(curQuad.position());

          const double integrationElement = intersection.geometry().integrationElement(curQuad.position());

          // The value of the local function
          const auto u = uFunction.evaluate(quadPos);

          // Value of the Neumann data at the current position
          auto neumannValue = (*neumannBoundaryLoad)(toEigen(intersection.geometry().global(curQuad.position())), lambda);

          energy -= neumannValue.dot(u) * curQuad.weight() * integrationElement;
        }
      }

      return energy;
    }

    LocalView localView_;
    Dune::CachedLocalBasis<
        std::remove_cvref_t<decltype(std::declval<LocalView>().tree().child(0).finiteElement().localBasis())>>
        localBasis;
    std::optional<std::function<Eigen::Vector<double, Traits::worlddim>(const Eigen::Vector<double, Traits::worlddim>&,
                                                                        const double&)>>
        volumeLoad;
    std::optional<std::function<Eigen::Vector<double, Traits::worlddim>(const Eigen::Vector<double, Traits::worlddim>&,
                                                                        const double&)>>
        neumannBoundaryLoad;
    const BoundaryPatch<GridView>* neumannBoundary_;
    Material mat;
  };

}  // namespace Ikarus
