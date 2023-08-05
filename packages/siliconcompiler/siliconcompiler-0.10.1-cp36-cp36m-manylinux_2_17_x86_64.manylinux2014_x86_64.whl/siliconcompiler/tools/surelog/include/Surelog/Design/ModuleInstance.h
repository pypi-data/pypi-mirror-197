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
 * File:   ModuleInstance.h
 * Author: alain
 *
 * Created on October 16, 2017, 10:48 PM
 */

#ifndef SURELOG_MODULEINSTANCE_H
#define SURELOG_MODULEINSTANCE_H
#pragma once

#include <Surelog/Common/Containers.h>
#include <Surelog/Common/NodeId.h>
#include <Surelog/Design/ValuedComponentI.h>
#include <Surelog/SourceCompile/VObjectTypes.h>

#include <string_view>

namespace SURELOG {

class DesignComponent;
class FileContent;
class ModuleInstance;
class Netlist;
class Parameter;
class PathId;
class SymbolId;
class SymbolTable;

class ModuleInstance : public ValuedComponentI {
  SURELOG_IMPLEMENT_RTTI(ModuleInstance, ValuedComponentI)
 public:
  ModuleInstance(DesignComponent* definition, const FileContent* fileContent,
                 NodeId nodeId, ModuleInstance* parent,
                 std::string_view instName, std::string_view moduleName);
  ~ModuleInstance() override;

  typedef std::map<UHDM::module_array*, std::vector<ModuleInstance*>>
      ModuleArrayModuleInstancesMap;

  void addSubInstance(ModuleInstance* subInstance);
  std::vector<ModuleInstance*>& getAllSubInstances() {
    return m_allSubInstances;
  }
  ModuleArrayModuleInstancesMap& getModuleArrayModuleInstancesMap() {
    return m_moduleArrayModuleInstancesMap;
  }
  void setInstanceBinding(ModuleInstance* boundToInstance) {
    m_boundInstance = boundToInstance;
  }
  DesignComponent* getDefinition() { return m_definition; }
  unsigned int getNbChildren() const { return m_allSubInstances.size(); }
  ModuleInstance* getChildren(unsigned int i) {
    if (i < m_allSubInstances.size()) {
      return m_allSubInstances[i];
    } else {
      return nullptr;
    }
  }
  ModuleInstance* getParent() const { return m_parent; }
  const FileContent* getFileContent() const { return m_fileContent; }
  PathId getFileId() const;
  NodeId getNodeId() const { return m_nodeId; }
  unsigned int getLineNb() const;
  unsigned short getColumnNb() const;
  unsigned int getEndLineNb() const;
  unsigned short getEndColumnNb() const;
  VObjectType getType() const;
  VObjectType getModuleType() const;
  SymbolId getFullPathId(SymbolTable* symbols) const;
  SymbolId getInstanceId(SymbolTable* symbols) const;
  SymbolId getModuleNameId(SymbolTable* symbols) const;
  std::string getInstanceName() const;
  std::string getFullPathName() const;
  std::string getModuleName() const;
  unsigned int getDepth() const;

  void setNodeId(NodeId id) { m_nodeId = id; }  // Used for generate stmt
  void overrideParentChild(ModuleInstance* parent, ModuleInstance* interm,
                           ModuleInstance* child);
  Netlist* getNetlist() { return m_netlist; }
  void setNetlist(Netlist* netlist) { m_netlist = netlist; }

  std::vector<Parameter*>& getTypeParams() { return m_typeParams; }

  Value* getValue(std::string_view name,
                  ExprBuilder& exprBuilder) const override;
  UHDM::expr* getComplexValue(std::string_view name) const override;

  ModuleInstance* getInstanceBinding() { return m_boundInstance; }
  bool isElaborated() const { return m_elaborated; }
  void setElaborated() { m_elaborated = true; }

  void setOverridenParam(std::string_view name);
  bool isOverridenParam(std::string_view name) const;

  // DO NOT change the signature of this method, it is used in gdb for debug.
  std::string decompile(char* valueName) final;

  ModuleInstance* getChildByName(std::string_view name);

 private:
  DesignComponent* m_definition;
  std::vector<ModuleInstance*> m_allSubInstances;
  const FileContent* m_fileContent;
  NodeId m_nodeId;
  ModuleInstance* m_parent;
  std::string m_instName;  // Can carry the moduleName@instanceName if the
                           // module is undefined
  std::vector<Parameter*> m_typeParams;
  Netlist* m_netlist;
  ModuleInstance* m_boundInstance = nullptr;
  bool m_elaborated = false;
  std::set<std::string, StringViewCompare> m_overridenParams;
  ModuleArrayModuleInstancesMap m_moduleArrayModuleInstancesMap;
};

class ModuleInstanceFactory {
 public:
  ModuleInstance* newModuleInstance(DesignComponent* definition,
                                    const FileContent* fileContent,
                                    NodeId nodeId, ModuleInstance* parent,
                                    std::string_view instName,
                                    std::string_view moduleName);
};

}  // namespace SURELOG

#endif /* SURELOG_MODULEINSTANCE_H */
