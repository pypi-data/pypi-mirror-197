// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#include <iostream>
#include <map>

#ifdef _WIN32
#include <fcntl.h>
#include <io.h>
#endif

#include "convert.h"
#include "dictionary.h"
#include "scoped_timer.h"
#include "types.h"

int main() {
  // todo:
  // https://namu.wiki/w/%EC%99%84%EC%84%B1%ED%98%95/%EC%A4%91%EB%B3%B5%20%ED%95%9C%EC%9E%90

  // todo: python script that parses various dictionary formats.

  // todo: 음이 중복된다면?

#ifdef _WIN32
  int ret = _setmode(_fileno(stdin), _O_WTEXT);

  if (!ret) {
    std::cerr << "Failed to _setmode()." << std::endl;
  }
  hanja::compat::string path =
      L"C:\\Users\\moonsik.park_estsoft\\Desktop\\hanja.txt";
  hanja::compat::string path_char =
      L"C:\\Users\\moonsik.park_estsoft\\Desktop\\hanja.txt";
#else
  hanja::compat::string path =
      "/home/moonsikpark/libhanja/src/pyhanja/data/hanja.txt";
  hanja::compat::string path_char =
      "/home/moonsikpark/libhanja/src/pyhanja/data/ks_normalize.txt";
#endif

  hanja::dictionary::Dictionary dict;

  dict.add_data(true, path);
  dict.add_data(false, path_char);

  hanja::compat::string input;
  while (true) {
#ifdef _WIN32
    std::getline(std::wcin, input);
#else
    std::getline(std::cin, input);
#endif

    ScopedTimer timer;

    hanja::compat::string match =
        hanja::convert::Convert(input, dict).to_korean_with_hanja("<", ">");

#ifdef _WIN32
    std::wcout << match << std::endl;
    std::wcout << timer.elapsed().count() << " msec elapsed." << std::endl;
#else
    std::cout << match << std::endl;
    std::cout << timer.elapsed().count() << " msec elapsed." << std::endl;
#endif
  }

  return 0;
}
