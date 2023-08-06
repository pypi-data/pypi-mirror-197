// Copyright (c) 2022 ESTsoft Corp. All rights reserved.
#include <string>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "convert.h"
#include "dictionary.h"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(_pyhanja, m) {
  py::class_<hanja::dictionary::DictionaryItem>(m, "DictionaryItem")
      .def_property_readonly("key", &hanja::dictionary::DictionaryItem::get_key)
      .def_property_readonly("value",
                             &hanja::dictionary::DictionaryItem::get_value)
      .def("__repr__",
          [](const hanja::dictionary::DictionaryItem &i) {
              return "<pyhanja.DictionaryItem key=" + i.get_key() + " value=" + i.get_value() + ">";
          }
      );

  py::class_<hanja::dictionary::Dictionary>(m, "Dictionary")
      .def(py::init<>())
      .def("add_data", &hanja::dictionary::Dictionary::add_data)
      .def("query", &hanja::dictionary::Dictionary::query)
      .def_property_readonly("size", &hanja::dictionary::Dictionary::size)
      .def("__repr__",
          [](const hanja::dictionary::Dictionary &i) {
              return "<pyhanja.Dictionary size=" + std::to_string(i.size()) + ">";
          }
      );

  py::class_<hanja::convert::Convert>(m, "Convert")
      .def(py::init<const hanja::compat::string &,
                    const hanja::dictionary::Dictionary &>())
      .def("to_korean", &hanja::convert::Convert::to_korean)
      .def("to_korean_with_hanja",
           &hanja::convert::Convert::to_korean_with_hanja)
      .def_property_readonly("match_pos",
                             &hanja::convert::Convert::get_match_pos);

  py::class_<hanja::types::MatchPosition>(m, "MatchPosition")
      .def_property_readonly("pos", &hanja::types::MatchPosition::get_pos)
      .def_property_readonly("key", &hanja::types::MatchPosition::get_key)
      .def_property_readonly("value", &hanja::types::MatchPosition::get_value)
      .def("__repr__",
          [](const hanja::types::MatchPosition &i) {
              return "<pyhanja.MatchPosition pos=" + std::to_string(i.get_pos()) + " key='" + i.get_key() + "' value=" + i.get_value() + "'>";
          }
      );

#ifdef VERSION_INFO
  m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
  m.attr("__version__") = "dev";
#endif
}
