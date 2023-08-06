// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#include "convert.h"

#include <algorithm>
#include <regex>

#include "dictionary.h"
#include "step/suffix_tree.hpp"

namespace hanja {
namespace convert {

Convert::Convert(const compat::string &input,
                 const dictionary::Dictionary &dict) noexcept
    : m_input(input), m_match_changed(input.length(), false) {
  replace_char(dict);
  find_match(dict);
}

void Convert::replace_char(const dictionary::Dictionary &dict) noexcept {
  for (const auto& [key, item] : dict.char_dict()) {
    for (auto at = m_input.find(item.get_key(), 0); at != std::string::npos;
         at = m_input.find(item.get_key(), at + item.get_value().length())) {
      m_input.replace(at, item.get_key().length(), item.get_value());
    }
  }
}

void Convert::find_match(const dictionary::Dictionary &dict) noexcept {
  // Build a suffix tree.
  step::suffix_tree<compat::char_t> tree;
  std::copy(m_input.begin(), m_input.end(), std::back_inserter(tree));

  // Find all matching words in a dictionary and save the position.

  /* HACK: This method does not store all positions for a given word. For
   * example, if the word is "banana" and the key is "na", while it should
   * return position 3 and 5, it returns only the position 3.
   *
   * To overcome this limitation, we should not rely on the position found here.
   * Instead, we should look up the key in the sentence manually.
   */
  for (const auto &[key, value] : dict.word_dict()) {
    std::vector<std::size_t> results;
    tree.find_all(key, std::back_inserter(results));
    if (results.size() > 0) {
      m_match.emplace_back(dict.query(key));
    }
  }

  // Sort by key descending.
  std::sort(m_match.begin(), m_match.end(),
            std::greater<dictionary::DictionaryItem>());

  /* Find MatchPositions using Match array and the input. We need the
   * m_match_changed vector because there are multiple matches that overlap and
   * we don't want them to change the same letter.
   *
   * For two matches "金:김" and "金屬:금속" for a word "金屬", we don't want
   * the both to apply their own pronunciations.
   */

  for (const auto &match : m_match) {
    // Look up the key in the sentence manually.
    auto key = match.get_key();

    compat::string::size_type pos = 0;
    while ((pos = m_input.find(key, pos)) != compat::string::npos) {
      bool overlap = false;

      // Check whether the key overlaps with a longer key previously found.
      for (std::size_t idx = pos; idx < pos + key.length(); idx++) {
        if (m_match_changed[idx]) {
          overlap = true;
          break;
        }
      }

      // No overlaps. We should replace this key with value.
      if (!overlap) {
        // Write the positions of the key we found to the changed vector.
        for (std::size_t idx = pos; idx < pos + key.length(); idx++) {
          m_match_changed[idx] = true;
        }

        // Create MatchPosition with the position.
        m_match_pos.push_back(match.to_match_position(pos));
      }
      pos += key.size();
    }
  }

  // Sort MatchPositions by position ascending.
  std::sort(m_match_pos.begin(), m_match_pos.end(),
            std::less<types::MatchPosition>());
}

const compat::string Convert::to_korean() const {
  // If we have no match, return the original string.
  if (m_match_pos.size() == 0) {
    return m_input;
  }

  compat::stringstream ss;
  std::size_t current_pos = 0;
  for (const auto &match_position : m_match_pos) {
    // Add a substring of current position ~ match position to the buffer
    ss << m_input.substr(current_pos, match_position.get_pos() - current_pos);
    // Add key's value to the buffer
    ss << match_position.get_value();
    // Update the current position
    current_pos = match_position.get_end_pos_original();
  }

  // Add a substring of current position ~ end of input string to the buffer
  ss << m_input.substr(current_pos, m_input.length() - current_pos);
  return ss.str();
}

const compat::string Convert::to_korean_with_hanja(
    const compat::string &delimiter_start,
    const compat::string &delimiter_end) const {
  if (m_match_pos.size() == 0) {
    return m_input;
  }

  compat::stringstream ss;
  std::size_t current_pos = 0;
  for (const auto &match_position : m_match_pos) {
    // Add a substring of current position ~ match position to the buffer
    ss << m_input.substr(current_pos, match_position.get_pos() - current_pos);
    // Add key's value to the buffer
    ss << match_position.get_value();
    ss << delimiter_start;
    // Add key to the buffer
    ss << match_position.get_key();
    ss << delimiter_end;
    // Update the current position
    current_pos = match_position.get_end_pos_original();
  }

  // Add a substring of current position ~ end of input string to the buffer
  ss << m_input.substr(current_pos, m_input.length() - current_pos);
  return ss.str();
}

}  // namespace convert
}  // namespace hanja
