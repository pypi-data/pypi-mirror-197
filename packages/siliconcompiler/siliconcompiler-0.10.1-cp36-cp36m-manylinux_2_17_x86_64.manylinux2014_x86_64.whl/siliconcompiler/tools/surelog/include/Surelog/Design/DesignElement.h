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
 * File:   DesignElement.h
 * Author: alain
 *
 * Created on June 8, 2017, 8:05 PM
 */

#ifndef SURELOG_DESIGNELEMENT_H
#define SURELOG_DESIGNELEMENT_H
#pragma once

#include <Surelog/Common/NodeId.h>
#include <Surelog/Common/PathId.h>
#include <Surelog/Common/SymbolId.h>
#include <Surelog/Design/TimeInfo.h>

#include <ostream>

namespace SURELOG {

class DesignElement final {
 public:
  enum ElemType {
    Module,
    Primitive,
    Interface,
    Program,
    Package,
    Config,
    Checker,
    Class,     // Class is not a Design element per Standard, but is a major
               // component tracked
    Function,  // Function is not a Design Element per Standard, but in a
               // package it is a element worth tracking
    Task,
    SLline  // Used to split files with correct file info
  };

  DesignElement(SymbolId name, PathId fileId, ElemType type, NodeId uniqueId,
                unsigned int line, unsigned short column, unsigned int endLine,
                unsigned short endColumn, NodeId parent);

  SymbolId m_name;
  PathId m_fileId;
  const ElemType m_type;
  const NodeId m_uniqueId;
  const unsigned int m_line;
  const unsigned short m_column;
  const unsigned int m_endLine;
  const unsigned short m_endColumn;
  NodeId m_parent;

  TimeInfo m_timeInfo;
  NodeId m_node;
  VObjectType m_defaultNetType = slNetType_Wire;
  void* m_context;  // Not persisted field, only used to build the DesignElement
                    // -> VNode relation
};

std::ostream& operator<<(std::ostream& os, DesignElement::ElemType type);

}  // namespace SURELOG

#endif /* SURELOG_DESIGNELEMENT_H */
