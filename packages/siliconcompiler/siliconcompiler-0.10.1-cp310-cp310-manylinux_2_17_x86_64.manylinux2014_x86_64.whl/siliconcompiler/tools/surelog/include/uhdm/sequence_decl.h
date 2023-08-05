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
 * File:   sequence_decl.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_SEQUENCE_DECL_H
#define UHDM_SEQUENCE_DECL_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/BaseClass.h>

#include "sequence_expr_multiclock_group.h"


namespace UHDM {


class sequence_decl final : public BaseClass {
  UHDM_IMPLEMENT_RTTI(sequence_decl, BaseClass)
public:
  // Implicit constructor used to initialize all members,
  // comment: sequence_decl();
  virtual ~sequence_decl() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  virtual bool VpiName(const std::string& data) final;

  virtual const std::string& VpiName() const final;

  bool VpiFullName(const std::string& data);

  const std::string& VpiFullName() const;

  VectorOfattribute* Attributes() const { return attributes_; }

  bool Attributes(VectorOfattribute* data) { attributes_ = data; return true; }

  VectorOfvariables* Variables() const { return variables_; }

  bool Variables(VectorOfvariables* data) { variables_ = data; return true; }

  const any* Sequence_expr_multiclock_group() const { return sequence_expr_multiclock_group_; }

  bool Sequence_expr_multiclock_group(any* data) { if (!sequence_expr_multiclock_groupGroupCompliant(data)) return false; sequence_expr_multiclock_group_ = data; return true; }

  VectorOfseq_formal_decl* Seq_formal_decls() const { return seq_formal_decls_; }

  bool Seq_formal_decls(VectorOfseq_formal_decl* data) { seq_formal_decls_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiSequenceDecl; }

  virtual sequence_decl* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdmsequence_decl; }

protected:
  void DeepCopy(sequence_decl* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  SymbolFactory::ID vpiName_ = 0;

  SymbolFactory::ID vpiFullName_ = 0;

  VectorOfattribute* attributes_ = nullptr;

  VectorOfvariables* variables_ = nullptr;

  any* sequence_expr_multiclock_group_ = nullptr;

  VectorOfseq_formal_decl* seq_formal_decls_ = nullptr;
};


typedef FactoryT<sequence_decl> sequence_declFactory;


typedef FactoryT<std::vector<sequence_decl *>> VectorOfsequence_declFactory;

}  // namespace UHDM

#endif
