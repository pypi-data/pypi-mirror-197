/*
 Copyright 2019 Alain Dargelas

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

/*
 * File:   Library.h
 * Author: alain
 *
 * Created on January 27, 2018, 5:25 PM
 */

#ifndef SURELOG_LIBRARY_H
#define SURELOG_LIBRARY_H
#pragma once

#include <Surelog/Common/PathId.h>

#include <map>
#include <set>
#include <string>
#include <vector>

namespace SURELOG {

class ModuleDefinition;
class SymbolTable;

class Library final {
 public:
  Library(std::string_view name, SymbolTable* symbols)
      : m_name(name), m_symbols(symbols) {}

  void addFileId(PathId fid) {
    m_fileIds.push_back(fid);
    m_fileIdsSet.insert(fid);
  }

  const std::string& getName() const { return m_name; }
  const PathIdVector& getFiles() const { return m_fileIds; }
  bool isMember(PathId fid) const {
    return m_fileIdsSet.find(fid) != m_fileIdsSet.end();
  }
  std::string report(SymbolTable* symbols) const;
  void addModuleDefinition(ModuleDefinition* def);
  std::map<std::string, ModuleDefinition*>& getModules() { return m_modules; }
  ModuleDefinition* getModule(const std::string& name) const;
  SymbolTable* getSymbols() const { return m_symbols; }

 private:
  std::string m_name;
  PathIdVector m_fileIds;
  PathIdSet m_fileIdsSet;
  std::map<std::string, ModuleDefinition*> m_modules;
  SymbolTable* const m_symbols;
};

}  // namespace SURELOG

#endif /* SURELOG_LIBRARY_H */
