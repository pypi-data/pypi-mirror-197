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
 * File:   Design.h
 * Author: alain
 *
 * Created on July 1, 2017, 1:23 PM
 */

#ifndef SURELOG_DESIGN_H
#define SURELOG_DESIGN_H
#pragma once

#include <Surelog/Common/Containers.h>
#include <Surelog/Common/NodeId.h>
#include <Surelog/Common/PathId.h>

#include <map>
#include <mutex>
#include <vector>

namespace SURELOG {

class AnalyzeFile;
class BindStmt;
class Builtin;
class CompileDesign;
class Compiler;
class ConfigSet;
class DefParam;
class DesignComponent;
class DesignElaboration;
class ErrorContainer;
class FileContent;
class LibrarySet;
class ModuleInstance;
class ParseCache;
class ParseFile;
class PPCache;
class PreprocessFile;
class SV3_1aPpTreeShapeListener;
class SV3_1aTreeShapeListener;
class SVLibShapeListener;
class Value;

class Design final {
  friend class AnalyzeFile;
  friend class Builtin;
  friend class CompileDesign;
  friend class Compiler;
  friend class DesignElaboration;
  friend class ParseCache;
  friend class ParseFile;
  friend class PPCache;
  friend class PreprocessFile;
  friend class SV3_1aPpTreeShapeListener;
  friend class SV3_1aTreeShapeListener;
  friend class SVLibShapeListener;

 public:
  Design(ErrorContainer* errors, LibrarySet* librarySet, ConfigSet* configSet)
      : m_errors(errors), m_librarySet(librarySet), m_configSet(configSet) {}

  Design(const Design& orig) = delete;

  ~Design();

  typedef std::vector<std::pair<PathId, FileContent*>> FileIdDesignContentMap;

  // TODO: Unfortunately, all these need to be non-const, as there is code
  // on the receiving end is not using const stringently enough.
  // Fix longer term.
  FileIdDesignContentMap& getAllFileContents() { return m_fileContents; }

  FileIdDesignContentMap& getAllPPFileContents() { return m_ppFileContents; }

  LibrarySet* getLibrarySet() const { return m_librarySet; }

  ConfigSet* getConfigSet() const { return m_configSet; }

  ModuleNameModuleDefinitionMap& getModuleDefinitions() {
    return m_moduleDefinitions;
  }

  PackageNamePackageDefinitionMultiMap& getPackageDefinitions() {
    return m_packageDefinitions;
  }

  PackageDefinitionVec& getOrderedPackageDefinitions() {
    return m_orderedPackageDefinitions;
  }

  ProgramNameProgramDefinitionMap& getProgramDefinitions() {
    return m_programDefinitions;
  }

  ClassNameClassDefinitionMultiMap& getClassDefinitions() {
    return m_classDefinitions;
  }

  ClassNameClassDefinitionMap& getUniqueClassDefinitions() {
    return m_uniqueClassDefinitions;
  }

  ModuleDefinition* getModuleDefinition(const std::string& moduleName) const;

  DesignComponent* getComponentDefinition(
      const std::string& componentName) const;

  const std::vector<ModuleInstance*>& getTopLevelModuleInstances() const {
    return m_topLevelModuleInstances;
  }

  std::string reportInstanceTree() const;

  void reportInstanceTreeStats(unsigned int& nbTopLevelModules,
                               unsigned int& maxDepth,
                               unsigned int& numberOfInstances,
                               unsigned int& numberOfLeafInstances,
                               unsigned int& nbUndefinedModules,
                               unsigned int& nbUndefinedInstances) const;

  DefParam* getDefParam(const std::string& name) const;

  Value* getDefParamValue(const std::string& name);

  std::map<std::string, DefParam*>& getDefParams() { return m_defParams; }

  void checkDefParamUsage(DefParam* parent = nullptr);

  ModuleInstance* findInstance(const std::vector<std::string>& path,
                               ModuleInstance* scope = nullptr) const;

  ModuleInstance* findInstance(const std::string& path,
                               ModuleInstance* scope = nullptr) const;

  Package* getPackage(std::string_view name) const;

  Program* getProgram(std::string_view name) const;

  ClassDefinition* getClassDefinition(const std::string& name) const;

  ErrorContainer* getErrorContainer() { return m_errors; }

  typedef std::multimap<const std::string, BindStmt*> BindMap;

  BindMap& getBindMap() { return m_bindMap; }

  std::vector<BindStmt*> getBindStmts(const std::string& targetName);

  void addBindStmt(const std::string& targetName, BindStmt* stmt);

 protected:
  // Thread-safe
  void addFileContent(PathId fileId, FileContent* content);

  // Thread-safe
  void addPPFileContent(PathId fileId, FileContent* content);

  void addOrderedPackage(const std::string& packageName) {
    m_orderedPackageNames.push_back(packageName);
  }

  void addModuleDefinition(const std::string& moduleName,
                           ModuleDefinition* def) {
    m_moduleDefinitions.insert(std::make_pair(moduleName, def));
  }

  void addTopLevelModuleInstance(ModuleInstance* instance) {
    m_topLevelModuleInstances.push_back(instance);
  }

  void addDefParam(const std::string& name, const FileContent* fC,
                   NodeId nodeId, Value* value);

  void addClassDefinition(const std::string& className,
                          ClassDefinition* classDef);

  void addProgramDefinition(const std::string programName, Program* program) {
    m_programDefinitions.insert(std::make_pair(programName, program));
  }

  Package* addPackageDefinition(const std::string& packageName,
                                Package* package);

  void clearContainers();

  void orderPackages();

 private:
  ModuleInstance* findInstance_(const std::vector<std::string>& path,
                                ModuleInstance* scope) const;
  void addDefParam_(std::vector<std::string>& path, const FileContent* fC,
                    NodeId nodeId, Value* value, DefParam* parent);
  DefParam* getDefParam_(std::vector<std::string>& path,
                         DefParam* parent) const;

  ErrorContainer* m_errors;

  LibrarySet* m_librarySet;

  ConfigSet* m_configSet;

  FileIdDesignContentMap m_fileContents;

  FileIdDesignContentMap m_ppFileContents;

  ModuleNameModuleDefinitionMap m_moduleDefinitions;

  std::vector<ModuleInstance*> m_topLevelModuleInstances;

  std::map<std::string, DefParam*> m_defParams;

  PackageNamePackageDefinitionMultiMap m_packageDefinitions;

  PackageDefinitionVec m_orderedPackageDefinitions;

  ProgramNameProgramDefinitionMap m_programDefinitions;

  ClassNameClassDefinitionMultiMap m_classDefinitions;

  ClassNameClassDefinitionMap m_uniqueClassDefinitions;

  std::vector<std::string> m_orderedPackageNames;

  BindMap m_bindMap;

  std::mutex m_mutex;
};

}  // namespace SURELOG

#endif /* SURELOG_DESIGN_H */
