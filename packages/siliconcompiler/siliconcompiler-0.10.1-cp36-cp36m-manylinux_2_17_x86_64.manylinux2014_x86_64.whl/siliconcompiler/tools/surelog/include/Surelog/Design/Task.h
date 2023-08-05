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
 * File:   Task.h
 * Author: alain
 *
 * Created on February 21, 2019, 8:19 PM
 */

#ifndef SURELOG_TASK_H
#define SURELOG_TASK_H
#pragma once

#include <Surelog/Common/SymbolId.h>
#include <Surelog/Design/Function.h>

#include <string>

namespace SURELOG {

class DesignComponent;
class FileContent;

class Task : public Procedure {
  SURELOG_IMPLEMENT_RTTI(Task, Procedure)
 public:
  Task(DesignComponent* parent, const FileContent* fC, NodeId id,
       const std::string& name)
      : Procedure(parent, fC, id, name) {}
  ~Task() override = default;

  bool compile(CompileHelper& compile_helper);
};

}  // namespace SURELOG

#endif /* SURELOG_TASK_H */
