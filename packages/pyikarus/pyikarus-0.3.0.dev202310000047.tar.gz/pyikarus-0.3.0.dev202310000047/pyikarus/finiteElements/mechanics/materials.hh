// SPDX-FileCopyrightText: 2022 The Ikarus Developers mueller@ibb.uni-stuttgart.de
// SPDX-License-Identifier: LGPL-3.0-or-later

#pragma once

#include "materials/interface.hh"
#include "materials/linearElasticity.hh"
#include "materials/neohooke.hh"
#include "materials/svk.hh"
#include "materials/tags.hh"
#include "materials/vanishingStress.hh"
#include "nonLinearElastic.hh"

//#include <dune/functions/functionspacebases/defaultglobalbasis.hh>
//#include <dune/functions/functionspacebases/powerbasis.hh>
//#include <dune/functions/functionspacebases/lagrangebasis.hh>
//#include <dune/grid/yaspgrid.hh>

namespace Ikarus {
  template <typename MaterialImpl>
  auto plainStress(const MaterialImpl& mat, typename MaterialImpl::ScalarType p_tol = 1e-8) {
    return makeVanishingStress<{2, 1}, {2, 0}, {2, 2}>(mat, p_tol);
  }

  template <typename MaterialImpl>
  auto shellMaterial(const MaterialImpl& mat, typename MaterialImpl::ScalarType p_tol = 1e-8) {
    return makeVanishingStress<{2, 2}>(mat, p_tol);
  }

  template <typename MaterialImpl>
  auto beamMaterial(const MaterialImpl& mat, typename MaterialImpl::ScalarType p_tol = 1e-8) {

//    using Type = Ikarus::NonLinearElastic<Dune::Functions::DefaultGlobalBasis<
//                     Dune::Functions::PowerPreBasis< Dune::Functions::BasisBuilder::FlatLexicographic ,
//                                                    Dune::Functions::LagrangePreBasis< Dune::YaspGrid< 2, Dune::EquidistantOffsetCoordinates< double, 2 > >::LeafGridView , 1 > , 2 > >,
//          Ikarus::VanishingStress<std::array<Ikarus::Impl::StressIndexPair, 3ul>{{Ikarus::Impl::StressIndexPair{2ul, 1ul}, Ikarus::Impl::StressIndexPair{2ul,0ul}, Ikarus::Impl::StressIndexPair{2ul, 2ul}}},Ikarus::NeoHooke<double> ,
//              Ikarus::FErequirements<Eigen::Ref<Eigen::VectorXd>>,true>;

    return makeVanishingStress<{1, 1}, {2, 2}>(mat, p_tol);
  }
}  // namespace Ikarus
