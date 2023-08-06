// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#ifndef LIBHANJA_TYPES_H_
#define LIBHANJA_TYPES_H_

#include <cstddef>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

namespace hanja {

namespace compat {
#ifdef _WIN32
using char_t = wchar_t;
#else
using char_t = char;
#endif
using string = std::basic_string<char_t>;
using ifstream = std::basic_ifstream<char_t>;
using stringstream = std::basic_stringstream<char_t>;
}  // namespace compat

namespace types {

class MatchPosition {
 public:
  MatchPosition() = delete;
  MatchPosition(const MatchPosition&) = default;
  MatchPosition& operator=(const MatchPosition&) = default;
  MatchPosition(MatchPosition&& p) noexcept = default;
  MatchPosition& operator=(MatchPosition&& p) = default;

  /* We need to compare the length of key and value in order to "replace" a
   * character.
   *
   * For example in a case where key="𥮗"("F0 A5 AE 97", length=4)
   * and value="국"("EA B5 AD", length=3) length mismatch, it is not possible to
   * simply insert the value data to the key's position. If we do that, we will
   * end up with "EA B5 AD 97". This will be encoded to 국� because U+97 does
   * not exist.
   *
   */
  MatchPosition(const std::size_t pos, const compat::string& value,
                const compat::string& key) noexcept;

  inline const std::size_t get_pos() const { return m_pos; }

  inline const compat::string& get_key() const { return m_key; }

  inline const compat::string& get_value() const { return m_value; }

  inline const std::ptrdiff_t kv_size_delta() const {
    return m_key.length() - m_value.length();
  }

  inline const std::size_t get_end_pos_original() const {
    return m_pos + m_value.length() + kv_size_delta();
  }

  inline auto operator<=>(const MatchPosition& other) const {
    return this->get_pos() <=> other.get_pos();
  }

 private:
  // TODO: ref to Match?
  compat::string m_key;
  compat::string m_value;
  std::size_t m_pos;
};

}  // namespace types
}  // namespace hanja

#endif  // LIBHANJA_TYPES_H_
