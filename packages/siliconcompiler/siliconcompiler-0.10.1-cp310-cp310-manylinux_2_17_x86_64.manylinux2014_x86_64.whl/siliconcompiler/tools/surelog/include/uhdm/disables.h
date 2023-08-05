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
 * File:   disables.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_DISABLES_H
#define UHDM_DISABLES_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/atomic_stmt.h>




namespace UHDM {


class disables : public atomic_stmt {
  UHDM_IMPLEMENT_RTTI(disables, atomic_stmt)
public:
  // Implicit constructor used to initialize all members,
  // comment: disables();
  virtual ~disables() = default;

  virtual disables* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override = 0;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const override { return uhdmdisables; }

protected:
  void DeepCopy(disables* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:

};

#if 0 // This class cannot be instantiated
typedef FactoryT<disables> disablesFactory;
#endif

typedef FactoryT<std::vector<disables *>> VectorOfdisablesFactory;

}  // namespace UHDM

#endif
