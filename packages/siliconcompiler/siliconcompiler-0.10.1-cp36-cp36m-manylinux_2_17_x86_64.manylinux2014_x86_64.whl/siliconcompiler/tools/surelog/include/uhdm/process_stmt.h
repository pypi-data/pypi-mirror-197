/*
 Do not modify, auto-generated by model_gen.tcl

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
 * File:   process_stmt.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_PROCESS_STMT_H
#define UHDM_PROCESS_STMT_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/BaseClass.h>

#include "stmt.h"


namespace UHDM {
class module;

class process_stmt : public BaseClass {
  UHDM_IMPLEMENT_RTTI(process_stmt, BaseClass)
public:
  // Implicit constructor used to initialize all members,
  // comment: process_stmt();
  virtual ~process_stmt() = default;

  const any* Stmt() const { return stmt_; }

  bool Stmt(any* data) { if (!stmtGroupCompliant(data)) return false; stmt_ = data; return true; }

  const module* Module() const { return module_; }

  bool Module(module* data) { module_ = data; return true; }

  VectorOfattribute* Attributes() const { return attributes_; }

  bool Attributes(VectorOfattribute* data) { attributes_ = data; return true; }

  virtual process_stmt* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override = 0;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const override { return uhdmprocess_stmt; }

protected:
  void DeepCopy(process_stmt* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  any* stmt_ = nullptr;

  module* module_ = nullptr;

  VectorOfattribute* attributes_ = nullptr;
};

#if 0 // This class cannot be instantiated
typedef FactoryT<process_stmt> process_stmtFactory;
#endif

typedef FactoryT<std::vector<process_stmt *>> VectorOfprocess_stmtFactory;

}  // namespace UHDM

#endif
