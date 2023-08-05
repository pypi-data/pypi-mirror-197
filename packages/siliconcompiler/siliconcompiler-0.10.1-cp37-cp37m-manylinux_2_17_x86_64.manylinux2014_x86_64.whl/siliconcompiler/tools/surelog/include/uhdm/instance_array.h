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
 * File:   instance_array.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_INSTANCE_ARRAY_H
#define UHDM_INSTANCE_ARRAY_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/BaseClass.h>




namespace UHDM {
class expr;
class typespec;

class instance_array : public BaseClass {
  UHDM_IMPLEMENT_RTTI(instance_array, BaseClass)
public:
  // Implicit constructor used to initialize all members,
  // comment: instance_array();
  virtual ~instance_array() = default;

  virtual bool VpiName(const std::string& data) final;

  virtual const std::string& VpiName() const final;

  bool VpiFullName(const std::string& data);

  const std::string& VpiFullName() const;

  int VpiSize() const { return vpiSize_; }

  bool VpiSize(int data) { vpiSize_ = data; return true; }

  const expr* Expr() const { return expr_; }

  bool Expr(expr* data) { expr_ = data; return true; }

  VectorOfrange* Ranges() const { return ranges_; }

  bool Ranges(VectorOfrange* data) { ranges_ = data; return true; }

  const expr* Left_expr() const { return left_expr_; }

  bool Left_expr(expr* data) { left_expr_ = data; return true; }

  const expr* Right_expr() const { return right_expr_; }

  bool Right_expr(expr* data) { right_expr_ = data; return true; }

  VectorOfinstance* Instances() const { return instances_; }

  bool Instances(VectorOfinstance* data) { instances_ = data; return true; }

  VectorOfmodule* Modules() const { return modules_; }

  bool Modules(VectorOfmodule* data) { modules_ = data; return true; }

  const typespec* Elem_typespec() const { return elem_typespec_; }

  bool Elem_typespec(typespec* data) { elem_typespec_ = data; return true; }

  virtual instance_array* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override = 0;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const override { return uhdminstance_array; }

protected:
  void DeepCopy(instance_array* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  SymbolFactory::ID vpiName_ = 0;

  SymbolFactory::ID vpiFullName_ = 0;

  int vpiSize_ = 0;

  expr* expr_ = nullptr;

  VectorOfrange* ranges_ = nullptr;

  expr* left_expr_ = nullptr;

  expr* right_expr_ = nullptr;

  VectorOfinstance* instances_ = nullptr;

  VectorOfmodule* modules_ = nullptr;

  typespec* elem_typespec_ = nullptr;
};

#if 0 // This class cannot be instantiated
typedef FactoryT<instance_array> instance_arrayFactory;
#endif

typedef FactoryT<std::vector<instance_array *>> VectorOfinstance_arrayFactory;

}  // namespace UHDM

#endif
