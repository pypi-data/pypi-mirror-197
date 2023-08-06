// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#include "types.h"

namespace hanja {
namespace types {

MatchPosition::MatchPosition(const std::size_t pos, const compat::string& key,
                             const compat::string& value) noexcept
    :  m_key(key), m_value(value), m_pos(pos) {}

}  // namespace types
}  // namespace hanja
