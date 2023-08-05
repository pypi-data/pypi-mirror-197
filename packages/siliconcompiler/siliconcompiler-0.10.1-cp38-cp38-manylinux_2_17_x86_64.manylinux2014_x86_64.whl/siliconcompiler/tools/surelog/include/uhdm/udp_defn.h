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
 * File:   udp_defn.h
 * Author:
 *
 * Created on December 14, 2019, 10:03 PM
 */

#ifndef UHDM_UDP_DEFN_H
#define UHDM_UDP_DEFN_H

#include <uhdm/sv_vpi_user.h>
#include <uhdm/uhdm_vpi_user.h>

#include <uhdm/containers.h>
#include <uhdm/BaseClass.h>




namespace UHDM {
class initial;

class udp_defn final : public BaseClass {
  UHDM_IMPLEMENT_RTTI(udp_defn, BaseClass)
public:
  // Implicit constructor used to initialize all members,
  // comment: udp_defn();
  virtual ~udp_defn() final = default;

  virtual const BaseClass* VpiParent() const final { return vpiParent_; }

  virtual bool VpiParent(BaseClass* data) final { vpiParent_ = data; return true; }

  virtual bool VpiFile(const std::string& data) final;

  virtual const std::string& VpiFile() const final;

  virtual unsigned int UhdmId() const final { return uhdmId_; }

  virtual bool UhdmId(unsigned int data) final { uhdmId_ = data; return true; }

  virtual bool VpiDefName(const std::string& data) final;

  virtual const std::string& VpiDefName() const final;

  int VpiSize() const { return vpiSize_; }

  bool VpiSize(int data) { vpiSize_ = data; return true; }

  bool VpiProtected() const { return vpiProtected_; }

  bool VpiProtected(bool data) { vpiProtected_ = data; return true; }

  int VpiPrimType() const { return vpiPrimType_; }

  bool VpiPrimType(int data) { vpiPrimType_ = data; return true; }

  VectorOfattribute* Attributes() const { return attributes_; }

  bool Attributes(VectorOfattribute* data) { attributes_ = data; return true; }

  VectorOfio_decl* Io_decls() const { return io_decls_; }

  bool Io_decls(VectorOfio_decl* data) { io_decls_ = data; return true; }

  VectorOftable_entry* Table_entrys() const { return table_entrys_; }

  bool Table_entrys(VectorOftable_entry* data) { table_entrys_ = data; return true; }

  const initial* Initial() const { return initial_; }

  bool Initial(initial* data) { initial_ = data; return true; }

  virtual unsigned int VpiType() const final { return vpiUdpDefn; }

  virtual udp_defn* DeepClone(Serializer* serializer, ElaboratorListener* elaborator, BaseClass* parent) const override;

  virtual const BaseClass* GetByVpiName(std::string_view name) const override;

  virtual std::tuple<const BaseClass*, UHDM_OBJECT_TYPE, const std::vector<const BaseClass*>*> GetByVpiType(int type) const override;

  virtual vpi_property_value_t GetVpiPropertyValue(int property) const override;

  virtual int Compare(const BaseClass* const other, AnySet& visited) const override;

  virtual  UHDM_OBJECT_TYPE UhdmType() const final { return uhdmudp_defn; }

protected:
  void DeepCopy(udp_defn* clone, Serializer* serializer,
                ElaboratorListener* elaborator, BaseClass* parent) const;

private:
  BaseClass* vpiParent_ = nullptr;

  SymbolFactory::ID vpiFile_ = 0;

  unsigned int uhdmId_ = 0;

  SymbolFactory::ID vpiDefName_ = 0;

  int vpiSize_ = 0;

  bool vpiProtected_ = false;

  int vpiPrimType_ = 0;

  VectorOfattribute* attributes_ = nullptr;

  VectorOfio_decl* io_decls_ = nullptr;

  VectorOftable_entry* table_entrys_ = nullptr;

  initial* initial_ = nullptr;
};


typedef FactoryT<udp_defn> udp_defnFactory;


typedef FactoryT<std::vector<udp_defn *>> VectorOfudp_defnFactory;

}  // namespace UHDM

#endif
