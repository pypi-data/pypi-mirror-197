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
 * File:   Struct.h
 * Author: alain
 *
 * Created on May 19, 2020, 11:55 AM
 */

#ifndef SURELOG_STRUCT_H
#define SURELOG_STRUCT_H
#pragma once

#include <Surelog/Common/SymbolId.h>
#include <Surelog/Design/DataType.h>
#include <Surelog/DesignCompile/CompileHelper.h>

#include <map>
#include <string>

namespace SURELOG {

class FileContent;

class Struct : public DataType {
  SURELOG_IMPLEMENT_RTTI(Struct, DataType)
 public:
  Struct(const FileContent* fC, NodeId nameId, NodeId structId);
  ~Struct() override = default;

  NodeId getNameId() const { return m_nameId; }

  bool isNet() const override;

 private:
  const NodeId m_nameId;
};

};  // namespace SURELOG

#endif /* SURELOG_STRUCT_H */
