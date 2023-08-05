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
 * File:   sequence_inst.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_SEQUENCE_INST_H
#define UHDM_SEQUENCE_INST_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/BaseClass.h>

#include "named_event_sequence_expr_group.h"


namespace UHDM {
class clocking_block;
class sequence_decl;

class sequence_inst final : public BaseClass {
  UHDM_IMPLEMENT_RTTI(sequence_inst, BaseClass)
public:
  // Implicit constructor used to initialize all members,
  // comment: sequence_inst();
  virtual ~sequence_inst() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  const sequence_decl* Sequence_decl() const { return sequence_decl_; }

  bool Sequence_decl(sequence_decl* data) { sequence_decl_ = data; return true; }

  VectorOfany* Named_event_sequence_expr_groups() const { return named_event_sequence_expr_groups_; }

  bool Named_event_sequence_expr_groups(VectorOfany* data) { if (!named_event_sequence_expr_groupGroupCompliant(data)) return false; named_event_sequence_expr_groups_ = data; return true; }

  int VpiStartLine() const { return vpiStartLine_; }

  bool VpiStartLine(int data) { vpiStartLine_ = data; return true; }

  int VpiColumn() const { return vpiColumn_; }

  bool VpiColumn(int data) { vpiColumn_ = data; return true; }

  int VpiEndLine() const { return vpiEndLine_; }

  bool VpiEndLine(int data) { vpiEndLine_ = data; return true; }

  int VpiEndColumn() const { return vpiEndColumn_; }

  bool VpiEndColumn(int data) { vpiEndColumn_ = data; return true; }

  virtual bool VpiName(const std::string& data) final;

  virtual const std::string& VpiName() const final;

  const clocking_block* Clocking_block() const { return clocking_block_; }

  bool Clocking_block(clocking_block* data) { clocking_block_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiSequenceInst; }

  virtual sequence_inst* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdmsequence_inst; }

protected:
  void DeepCopy(sequence_inst* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  sequence_decl* sequence_decl_ = nullptr;

  VectorOfany* named_event_sequence_expr_groups_ = nullptr;

  int vpiStartLine_ = 0;

  int vpiColumn_ = 0;

  int vpiEndLine_ = 0;

  int vpiEndColumn_ = 0;

  SymbolFactory::ID vpiName_ = 0;

  clocking_block* clocking_block_ = nullptr;
};


typedef FactoryT<sequence_inst> sequence_instFactory;


typedef FactoryT<std::vector<sequence_inst *>> VectorOfsequence_instFactory;

}  // namespace UHDM

#endif
