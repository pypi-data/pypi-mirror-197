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
 * File:   var_bit.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_VAR_BIT_H
#define UHDM_VAR_BIT_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/variables.h>




namespace UHDM {
class expr;

class var_bit final : public variables {
  UHDM_IMPLEMENT_RTTI(var_bit, variables)
public:
  // Implicit constructor used to initialize all members,
  // comment: var_bit();
  virtual ~var_bit() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  bool VpiConstantSelect() const { return vpiConstantSelect_; }

  bool VpiConstantSelect(bool data) { vpiConstantSelect_ = data; return true; }

  const expr* Expr_index() const { return expr_index_; }

  bool Expr_index(expr* data) { expr_index_ = data; return true; }

  VectorOfexpr* Expr_indexes() const { return expr_indexes_; }

  bool Expr_indexes(VectorOfexpr* data) { expr_indexes_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiVarBit; }

  virtual var_bit* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdmvar_bit; }

protected:
  void DeepCopy(var_bit* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  bool vpiConstantSelect_ = false;

  expr* expr_index_ = nullptr;

  VectorOfexpr* expr_indexes_ = nullptr;
};


typedef FactoryT<var_bit> var_bitFactory;


typedef FactoryT<std::vector<var_bit *>> VectorOfvar_bitFactory;

}  // namespace UHDM

#endif
