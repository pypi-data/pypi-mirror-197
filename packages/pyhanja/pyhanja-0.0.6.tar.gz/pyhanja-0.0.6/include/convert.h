// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#ifndef LIBHANJA_CONVERT_H_
#define LIBHANJA_CONVERT_H_

#include <string>
#include <vector>

#include "dictionary.h"
#include "types.h"

namespace hanja {
namespace convert {

class Convert {
 public:
  Convert() = delete;
  Convert(const Convert&) = delete;
  Convert& operator=(const Convert&) = delete;
  Convert(const compat::string& input,
          const dictionary::Dictionary& dict) noexcept;

  const compat::string to_korean() const;

  const compat::string to_korean_with_hanja(
      const compat::string& delimiter_start,
      const compat::string& delimiter_end) const;

  inline const compat::string input() const { return m_input; }

  inline const std::vector<types::MatchPosition>& get_match_pos() const {
    return m_match_pos;
  }

 private:
  void find_match(const dictionary::Dictionary& dict) noexcept;
  void replace_char(const dictionary::Dictionary& dict) noexcept;
  compat::string m_input;
  std::vector<dictionary::DictionaryItem> m_match;
  std::vector<bool> m_match_changed;
  std::vector<types::MatchPosition> m_match_pos;
};

}  // namespace convert
}  // namespace hanja

#endif  // LIBHANJA_CONVERT_H_
