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
 * File:   integer_typespec.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_INTEGER_TYPESPEC_H
#define UHDM_INTEGER_TYPESPEC_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/typespec.h>




namespace UHDM {
class expr;

class integer_typespec final : public typespec {
  UHDM_IMPLEMENT_RTTI(integer_typespec, typespec)
public:
  // Implicit constructor used to initialize all members,
  // comment: integer_typespec();
  virtual ~integer_typespec() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  bool VpiValue(const std::string& data);

  const std::string& VpiValue() const;

  const expr* Expr() const { return expr_; }

  bool Expr(expr* data) { expr_ = data; return true; }

  bool VpiSigned() const { return vpiSigned_; }

  bool VpiSigned(bool data) { vpiSigned_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiIntegerTypespec; }

  virtual integer_typespec* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdminteger_typespec; }

protected:
  void DeepCopy(integer_typespec* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  SymbolFactory::ID vpiValue_ = 0;

  expr* expr_ = nullptr;

  bool vpiSigned_ = false;
};


typedef FactoryT<integer_typespec> integer_typespecFactory;


typedef FactoryT<std::vector<integer_typespec *>> VectorOfinteger_typespecFactory;

}  // namespace UHDM

#endif
