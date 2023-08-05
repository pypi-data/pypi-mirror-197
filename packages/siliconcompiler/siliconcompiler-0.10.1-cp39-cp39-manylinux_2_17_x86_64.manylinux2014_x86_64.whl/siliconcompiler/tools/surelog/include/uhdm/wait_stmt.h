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
 * File:   wait_stmt.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_WAIT_STMT_H
#define UHDM_WAIT_STMT_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/waits.h>

#include "expr_sequence_inst_group.h"


namespace UHDM {


class wait_stmt final : public waits {
  UHDM_IMPLEMENT_RTTI(wait_stmt, waits)
public:
  // Implicit constructor used to initialize all members,
  // comment: wait_stmt();
  virtual ~wait_stmt() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  const any* VpiCondition() const { return vpiCondition_; }

  bool VpiCondition(any* data) { if (!expr_sequence_inst_groupGroupCompliant(data)) return false; vpiCondition_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiWait; }

  virtual wait_stmt* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdmwait_stmt; }

protected:
  void DeepCopy(wait_stmt* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  any* vpiCondition_ = nullptr;
};


typedef FactoryT<wait_stmt> wait_stmtFactory;


typedef FactoryT<std::vector<wait_stmt *>> VectorOfwait_stmtFactory;

}  // namespace UHDM

#endif
