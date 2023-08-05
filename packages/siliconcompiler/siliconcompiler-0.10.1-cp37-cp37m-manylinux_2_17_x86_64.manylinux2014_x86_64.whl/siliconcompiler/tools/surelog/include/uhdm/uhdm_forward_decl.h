// -*- c++ -*-

/*

 Copyright 2019-2020 Alain Dargelas

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
 * File:   uhdm_forward_decl.h
 * Author:
 *
 * Created on May 06, 2020, 10:03 PM
 */

#ifndef UHDM_FORWARD_DECL_H
#define UHDM_FORWARD_DECL_H

#include <vector>

#include <uhdm/BaseClass.h>

namespace UHDM {
class BaseClass;
typedef BaseClass any;

class alias_stmt;
class always;
class any_pattern;
class array_net;
class array_typespec;
class array_var;
class assert_stmt;
class assign_stmt;
class assignment;
class assume;
class atomic_stmt;
class attribute;
class begin;
class bit_select;
class bit_typespec;
class bit_var;
class break_stmt;
class byte_typespec;
class byte_var;
class case_item;
class case_property;
class case_property_item;
class case_stmt;
class chandle_typespec;
class chandle_var;
class checker_decl;
class checker_inst;
class checker_inst_port;
class checker_port;
class class_defn;
class class_obj;
class class_typespec;
class class_var;
class clocked_property;
class clocked_seq;
class clocking_block;
class clocking_io_decl;
class concurrent_assertions;
class constant;
class constr_foreach;
class constr_if;
class constr_if_else;
class constraint;
class constraint_expr;
class constraint_ordering;
class cont_assign;
class cont_assign_bit;
class continue_stmt;
class cover;
class deassign;
class def_param;
class delay_control;
class delay_term;
class design;
class disable;
class disable_fork;
class disables;
class dist_item;
class distribution;
class do_while;
class enum_const;
class enum_net;
class enum_typespec;
class enum_var;
class event_control;
class event_stmt;
class event_typespec;
class expect_stmt;
class expr;
class extends;
class final_stmt;
class for_stmt;
class force;
class foreach_stmt;
class forever_stmt;
class fork_stmt;
class func_call;
class function;
class gate;
class gate_array;
class gen_scope;
class gen_scope_array;
class gen_var;
class hier_path;
class if_else;
class if_stmt;
class immediate_assert;
class immediate_assume;
class immediate_cover;
class implication;
class import_typespec;
class include_file_info;
class indexed_part_select;
class initial;
class instance;
class instance_array;
class int_typespec;
class int_var;
class integer_net;
class integer_typespec;
class integer_var;
class interface;
class interface_array;
class interface_tf_decl;
class interface_typespec;
class io_decl;
class let_decl;
class let_expr;
class logic_net;
class logic_typespec;
class logic_var;
class long_int_typespec;
class long_int_var;
class method_func_call;
class method_task_call;
class mod_path;
class modport;
class module;
class module_array;
class module_typespec;
class multiclock_sequence_expr;
class named_begin;
class named_event;
class named_event_array;
class named_fork;
class net;
class net_bit;
class net_drivers;
class net_loads;
class nets;
class null_stmt;
class operation;
class ordered_wait;
class package;
class packed_array_net;
class packed_array_typespec;
class packed_array_var;
class param_assign;
class parameter;
class part_select;
class path_term;
class port;
class port_bit;
class ports;
class prim_term;
class primitive;
class primitive_array;
class process_stmt;
class program;
class program_array;
class prop_formal_decl;
class property_decl;
class property_inst;
class property_spec;
class property_typespec;
class range;
class real_typespec;
class real_var;
class ref_obj;
class ref_var;
class reg;
class reg_array;
class release;
class repeat;
class repeat_control;
class restrict;
class return_stmt;
class scope;
class seq_formal_decl;
class sequence_decl;
class sequence_inst;
class sequence_typespec;
class short_int_typespec;
class short_int_var;
class short_real_typespec;
class short_real_var;
class simple_expr;
class soft_disable;
class spec_param;
class string_typespec;
class string_var;
class struct_net;
class struct_pattern;
class struct_typespec;
class struct_var;
class switch_array;
class switch_tran;
class sys_func_call;
class sys_task_call;
class table_entry;
class tagged_pattern;
class task;
class task_call;
class task_func;
class tchk;
class tchk_term;
class tf_call;
class thread_obj;
class time_net;
class time_typespec;
class time_var;
class type_parameter;
class typespec;
class typespec_member;
class udp;
class udp_array;
class udp_defn;
class union_typespec;
class union_var;
class unsupported_expr;
class unsupported_stmt;
class unsupported_typespec;
class user_systf;
class var_bit;
class var_select;
class variables;
class virtual_interface_var;
class void_typespec;
class wait_fork;
class wait_stmt;
class waits;
class while_stmt;

typedef FactoryT<alias_stmt> alias_stmtFactory;
typedef FactoryT<always> alwaysFactory;
typedef FactoryT<any_pattern> any_patternFactory;
typedef FactoryT<array_net> array_netFactory;
typedef FactoryT<array_typespec> array_typespecFactory;
typedef FactoryT<array_var> array_varFactory;
typedef FactoryT<assert_stmt> assert_stmtFactory;
typedef FactoryT<assign_stmt> assign_stmtFactory;
typedef FactoryT<assignment> assignmentFactory;
typedef FactoryT<assume> assumeFactory;
typedef FactoryT<attribute> attributeFactory;
typedef FactoryT<begin> beginFactory;
typedef FactoryT<bit_select> bit_selectFactory;
typedef FactoryT<bit_typespec> bit_typespecFactory;
typedef FactoryT<bit_var> bit_varFactory;
typedef FactoryT<break_stmt> break_stmtFactory;
typedef FactoryT<byte_typespec> byte_typespecFactory;
typedef FactoryT<byte_var> byte_varFactory;
typedef FactoryT<case_item> case_itemFactory;
typedef FactoryT<case_property> case_propertyFactory;
typedef FactoryT<case_property_item> case_property_itemFactory;
typedef FactoryT<case_stmt> case_stmtFactory;
typedef FactoryT<chandle_typespec> chandle_typespecFactory;
typedef FactoryT<chandle_var> chandle_varFactory;
typedef FactoryT<checker_decl> checker_declFactory;
typedef FactoryT<checker_inst> checker_instFactory;
typedef FactoryT<checker_inst_port> checker_inst_portFactory;
typedef FactoryT<checker_port> checker_portFactory;
typedef FactoryT<class_defn> class_defnFactory;
typedef FactoryT<class_obj> class_objFactory;
typedef FactoryT<class_typespec> class_typespecFactory;
typedef FactoryT<class_var> class_varFactory;
typedef FactoryT<clocked_property> clocked_propertyFactory;
typedef FactoryT<clocked_seq> clocked_seqFactory;
typedef FactoryT<clocking_block> clocking_blockFactory;
typedef FactoryT<clocking_io_decl> clocking_io_declFactory;
typedef FactoryT<constant> constantFactory;
typedef FactoryT<constr_foreach> constr_foreachFactory;
typedef FactoryT<constr_if> constr_ifFactory;
typedef FactoryT<constr_if_else> constr_if_elseFactory;
typedef FactoryT<constraint> constraintFactory;
typedef FactoryT<constraint_ordering> constraint_orderingFactory;
typedef FactoryT<cont_assign> cont_assignFactory;
typedef FactoryT<cont_assign_bit> cont_assign_bitFactory;
typedef FactoryT<continue_stmt> continue_stmtFactory;
typedef FactoryT<cover> coverFactory;
typedef FactoryT<deassign> deassignFactory;
typedef FactoryT<def_param> def_paramFactory;
typedef FactoryT<delay_control> delay_controlFactory;
typedef FactoryT<delay_term> delay_termFactory;
typedef FactoryT<design> designFactory;
typedef FactoryT<disable> disableFactory;
typedef FactoryT<disable_fork> disable_forkFactory;
typedef FactoryT<dist_item> dist_itemFactory;
typedef FactoryT<distribution> distributionFactory;
typedef FactoryT<do_while> do_whileFactory;
typedef FactoryT<enum_const> enum_constFactory;
typedef FactoryT<enum_net> enum_netFactory;
typedef FactoryT<enum_typespec> enum_typespecFactory;
typedef FactoryT<enum_var> enum_varFactory;
typedef FactoryT<event_control> event_controlFactory;
typedef FactoryT<event_stmt> event_stmtFactory;
typedef FactoryT<event_typespec> event_typespecFactory;
typedef FactoryT<expect_stmt> expect_stmtFactory;
typedef FactoryT<extends> extendsFactory;
typedef FactoryT<final_stmt> final_stmtFactory;
typedef FactoryT<for_stmt> for_stmtFactory;
typedef FactoryT<force> forceFactory;
typedef FactoryT<foreach_stmt> foreach_stmtFactory;
typedef FactoryT<forever_stmt> forever_stmtFactory;
typedef FactoryT<fork_stmt> fork_stmtFactory;
typedef FactoryT<func_call> func_callFactory;
typedef FactoryT<function> functionFactory;
typedef FactoryT<gate> gateFactory;
typedef FactoryT<gate_array> gate_arrayFactory;
typedef FactoryT<gen_scope> gen_scopeFactory;
typedef FactoryT<gen_scope_array> gen_scope_arrayFactory;
typedef FactoryT<gen_var> gen_varFactory;
typedef FactoryT<hier_path> hier_pathFactory;
typedef FactoryT<if_else> if_elseFactory;
typedef FactoryT<if_stmt> if_stmtFactory;
typedef FactoryT<immediate_assert> immediate_assertFactory;
typedef FactoryT<immediate_assume> immediate_assumeFactory;
typedef FactoryT<immediate_cover> immediate_coverFactory;
typedef FactoryT<implication> implicationFactory;
typedef FactoryT<import_typespec> import_typespecFactory;
typedef FactoryT<include_file_info> include_file_infoFactory;
typedef FactoryT<indexed_part_select> indexed_part_selectFactory;
typedef FactoryT<initial> initialFactory;
typedef FactoryT<int_typespec> int_typespecFactory;
typedef FactoryT<int_var> int_varFactory;
typedef FactoryT<integer_net> integer_netFactory;
typedef FactoryT<integer_typespec> integer_typespecFactory;
typedef FactoryT<integer_var> integer_varFactory;
typedef FactoryT<interface> interfaceFactory;
typedef FactoryT<interface_array> interface_arrayFactory;
typedef FactoryT<interface_tf_decl> interface_tf_declFactory;
typedef FactoryT<interface_typespec> interface_typespecFactory;
typedef FactoryT<io_decl> io_declFactory;
typedef FactoryT<let_decl> let_declFactory;
typedef FactoryT<let_expr> let_exprFactory;
typedef FactoryT<logic_net> logic_netFactory;
typedef FactoryT<logic_typespec> logic_typespecFactory;
typedef FactoryT<logic_var> logic_varFactory;
typedef FactoryT<long_int_typespec> long_int_typespecFactory;
typedef FactoryT<long_int_var> long_int_varFactory;
typedef FactoryT<method_func_call> method_func_callFactory;
typedef FactoryT<method_task_call> method_task_callFactory;
typedef FactoryT<mod_path> mod_pathFactory;
typedef FactoryT<modport> modportFactory;
typedef FactoryT<module> moduleFactory;
typedef FactoryT<module_array> module_arrayFactory;
typedef FactoryT<module_typespec> module_typespecFactory;
typedef FactoryT<multiclock_sequence_expr> multiclock_sequence_exprFactory;
typedef FactoryT<named_begin> named_beginFactory;
typedef FactoryT<named_event> named_eventFactory;
typedef FactoryT<named_event_array> named_event_arrayFactory;
typedef FactoryT<named_fork> named_forkFactory;
typedef FactoryT<net_bit> net_bitFactory;
typedef FactoryT<null_stmt> null_stmtFactory;
typedef FactoryT<operation> operationFactory;
typedef FactoryT<ordered_wait> ordered_waitFactory;
typedef FactoryT<package> packageFactory;
typedef FactoryT<packed_array_net> packed_array_netFactory;
typedef FactoryT<packed_array_typespec> packed_array_typespecFactory;
typedef FactoryT<packed_array_var> packed_array_varFactory;
typedef FactoryT<param_assign> param_assignFactory;
typedef FactoryT<parameter> parameterFactory;
typedef FactoryT<part_select> part_selectFactory;
typedef FactoryT<path_term> path_termFactory;
typedef FactoryT<port> portFactory;
typedef FactoryT<port_bit> port_bitFactory;
typedef FactoryT<prim_term> prim_termFactory;
typedef FactoryT<program> programFactory;
typedef FactoryT<program_array> program_arrayFactory;
typedef FactoryT<prop_formal_decl> prop_formal_declFactory;
typedef FactoryT<property_decl> property_declFactory;
typedef FactoryT<property_inst> property_instFactory;
typedef FactoryT<property_spec> property_specFactory;
typedef FactoryT<property_typespec> property_typespecFactory;
typedef FactoryT<range> rangeFactory;
typedef FactoryT<real_typespec> real_typespecFactory;
typedef FactoryT<real_var> real_varFactory;
typedef FactoryT<ref_obj> ref_objFactory;
typedef FactoryT<ref_var> ref_varFactory;
typedef FactoryT<reg> regFactory;
typedef FactoryT<reg_array> reg_arrayFactory;
typedef FactoryT<release> releaseFactory;
typedef FactoryT<repeat> repeatFactory;
typedef FactoryT<repeat_control> repeat_controlFactory;
typedef FactoryT<restrict> restrictFactory;
typedef FactoryT<return_stmt> return_stmtFactory;
typedef FactoryT<seq_formal_decl> seq_formal_declFactory;
typedef FactoryT<sequence_decl> sequence_declFactory;
typedef FactoryT<sequence_inst> sequence_instFactory;
typedef FactoryT<sequence_typespec> sequence_typespecFactory;
typedef FactoryT<short_int_typespec> short_int_typespecFactory;
typedef FactoryT<short_int_var> short_int_varFactory;
typedef FactoryT<short_real_typespec> short_real_typespecFactory;
typedef FactoryT<short_real_var> short_real_varFactory;
typedef FactoryT<soft_disable> soft_disableFactory;
typedef FactoryT<spec_param> spec_paramFactory;
typedef FactoryT<string_typespec> string_typespecFactory;
typedef FactoryT<string_var> string_varFactory;
typedef FactoryT<struct_net> struct_netFactory;
typedef FactoryT<struct_pattern> struct_patternFactory;
typedef FactoryT<struct_typespec> struct_typespecFactory;
typedef FactoryT<struct_var> struct_varFactory;
typedef FactoryT<switch_array> switch_arrayFactory;
typedef FactoryT<switch_tran> switch_tranFactory;
typedef FactoryT<sys_func_call> sys_func_callFactory;
typedef FactoryT<sys_task_call> sys_task_callFactory;
typedef FactoryT<table_entry> table_entryFactory;
typedef FactoryT<tagged_pattern> tagged_patternFactory;
typedef FactoryT<task> taskFactory;
typedef FactoryT<task_call> task_callFactory;
typedef FactoryT<tchk> tchkFactory;
typedef FactoryT<tchk_term> tchk_termFactory;
typedef FactoryT<thread_obj> thread_objFactory;
typedef FactoryT<time_net> time_netFactory;
typedef FactoryT<time_typespec> time_typespecFactory;
typedef FactoryT<time_var> time_varFactory;
typedef FactoryT<type_parameter> type_parameterFactory;
typedef FactoryT<typespec_member> typespec_memberFactory;
typedef FactoryT<udp> udpFactory;
typedef FactoryT<udp_array> udp_arrayFactory;
typedef FactoryT<udp_defn> udp_defnFactory;
typedef FactoryT<union_typespec> union_typespecFactory;
typedef FactoryT<union_var> union_varFactory;
typedef FactoryT<unsupported_expr> unsupported_exprFactory;
typedef FactoryT<unsupported_stmt> unsupported_stmtFactory;
typedef FactoryT<unsupported_typespec> unsupported_typespecFactory;
typedef FactoryT<user_systf> user_systfFactory;
typedef FactoryT<var_bit> var_bitFactory;
typedef FactoryT<var_select> var_selectFactory;
typedef FactoryT<virtual_interface_var> virtual_interface_varFactory;
typedef FactoryT<void_typespec> void_typespecFactory;
typedef FactoryT<wait_fork> wait_forkFactory;
typedef FactoryT<wait_stmt> wait_stmtFactory;
typedef FactoryT<while_stmt> while_stmtFactory;

typedef FactoryT<std::vector<BaseClass*>> VectorOfanyFactory;
typedef FactoryT<std::vector<alias_stmt *>> VectorOfalias_stmtFactory;
typedef FactoryT<std::vector<always *>> VectorOfalwaysFactory;
typedef FactoryT<std::vector<any_pattern *>> VectorOfany_patternFactory;
typedef FactoryT<std::vector<array_net *>> VectorOfarray_netFactory;
typedef FactoryT<std::vector<array_typespec *>> VectorOfarray_typespecFactory;
typedef FactoryT<std::vector<array_var *>> VectorOfarray_varFactory;
typedef FactoryT<std::vector<assert_stmt *>> VectorOfassert_stmtFactory;
typedef FactoryT<std::vector<assign_stmt *>> VectorOfassign_stmtFactory;
typedef FactoryT<std::vector<assignment *>> VectorOfassignmentFactory;
typedef FactoryT<std::vector<assume *>> VectorOfassumeFactory;
typedef FactoryT<std::vector<atomic_stmt *>> VectorOfatomic_stmtFactory;
typedef FactoryT<std::vector<attribute *>> VectorOfattributeFactory;
typedef FactoryT<std::vector<begin *>> VectorOfbeginFactory;
typedef FactoryT<std::vector<bit_select *>> VectorOfbit_selectFactory;
typedef FactoryT<std::vector<bit_typespec *>> VectorOfbit_typespecFactory;
typedef FactoryT<std::vector<bit_var *>> VectorOfbit_varFactory;
typedef FactoryT<std::vector<break_stmt *>> VectorOfbreak_stmtFactory;
typedef FactoryT<std::vector<byte_typespec *>> VectorOfbyte_typespecFactory;
typedef FactoryT<std::vector<byte_var *>> VectorOfbyte_varFactory;
typedef FactoryT<std::vector<case_item *>> VectorOfcase_itemFactory;
typedef FactoryT<std::vector<case_property *>> VectorOfcase_propertyFactory;
typedef FactoryT<std::vector<case_property_item *>> VectorOfcase_property_itemFactory;
typedef FactoryT<std::vector<case_stmt *>> VectorOfcase_stmtFactory;
typedef FactoryT<std::vector<chandle_typespec *>> VectorOfchandle_typespecFactory;
typedef FactoryT<std::vector<chandle_var *>> VectorOfchandle_varFactory;
typedef FactoryT<std::vector<checker_decl *>> VectorOfchecker_declFactory;
typedef FactoryT<std::vector<checker_inst *>> VectorOfchecker_instFactory;
typedef FactoryT<std::vector<checker_inst_port *>> VectorOfchecker_inst_portFactory;
typedef FactoryT<std::vector<checker_port *>> VectorOfchecker_portFactory;
typedef FactoryT<std::vector<class_defn *>> VectorOfclass_defnFactory;
typedef FactoryT<std::vector<class_obj *>> VectorOfclass_objFactory;
typedef FactoryT<std::vector<class_typespec *>> VectorOfclass_typespecFactory;
typedef FactoryT<std::vector<class_var *>> VectorOfclass_varFactory;
typedef FactoryT<std::vector<clocked_property *>> VectorOfclocked_propertyFactory;
typedef FactoryT<std::vector<clocked_seq *>> VectorOfclocked_seqFactory;
typedef FactoryT<std::vector<clocking_block *>> VectorOfclocking_blockFactory;
typedef FactoryT<std::vector<clocking_io_decl *>> VectorOfclocking_io_declFactory;
typedef FactoryT<std::vector<concurrent_assertions *>> VectorOfconcurrent_assertionsFactory;
typedef FactoryT<std::vector<constant *>> VectorOfconstantFactory;
typedef FactoryT<std::vector<constr_foreach *>> VectorOfconstr_foreachFactory;
typedef FactoryT<std::vector<constr_if *>> VectorOfconstr_ifFactory;
typedef FactoryT<std::vector<constr_if_else *>> VectorOfconstr_if_elseFactory;
typedef FactoryT<std::vector<constraint *>> VectorOfconstraintFactory;
typedef FactoryT<std::vector<constraint_expr *>> VectorOfconstraint_exprFactory;
typedef FactoryT<std::vector<constraint_ordering *>> VectorOfconstraint_orderingFactory;
typedef FactoryT<std::vector<cont_assign *>> VectorOfcont_assignFactory;
typedef FactoryT<std::vector<cont_assign_bit *>> VectorOfcont_assign_bitFactory;
typedef FactoryT<std::vector<continue_stmt *>> VectorOfcontinue_stmtFactory;
typedef FactoryT<std::vector<cover *>> VectorOfcoverFactory;
typedef FactoryT<std::vector<deassign *>> VectorOfdeassignFactory;
typedef FactoryT<std::vector<def_param *>> VectorOfdef_paramFactory;
typedef FactoryT<std::vector<delay_control *>> VectorOfdelay_controlFactory;
typedef FactoryT<std::vector<delay_term *>> VectorOfdelay_termFactory;
typedef FactoryT<std::vector<design *>> VectorOfdesignFactory;
typedef FactoryT<std::vector<disable *>> VectorOfdisableFactory;
typedef FactoryT<std::vector<disable_fork *>> VectorOfdisable_forkFactory;
typedef FactoryT<std::vector<disables *>> VectorOfdisablesFactory;
typedef FactoryT<std::vector<dist_item *>> VectorOfdist_itemFactory;
typedef FactoryT<std::vector<distribution *>> VectorOfdistributionFactory;
typedef FactoryT<std::vector<do_while *>> VectorOfdo_whileFactory;
typedef FactoryT<std::vector<enum_const *>> VectorOfenum_constFactory;
typedef FactoryT<std::vector<enum_net *>> VectorOfenum_netFactory;
typedef FactoryT<std::vector<enum_typespec *>> VectorOfenum_typespecFactory;
typedef FactoryT<std::vector<enum_var *>> VectorOfenum_varFactory;
typedef FactoryT<std::vector<event_control *>> VectorOfevent_controlFactory;
typedef FactoryT<std::vector<event_stmt *>> VectorOfevent_stmtFactory;
typedef FactoryT<std::vector<event_typespec *>> VectorOfevent_typespecFactory;
typedef FactoryT<std::vector<expect_stmt *>> VectorOfexpect_stmtFactory;
typedef FactoryT<std::vector<expr *>> VectorOfexprFactory;
typedef FactoryT<std::vector<extends *>> VectorOfextendsFactory;
typedef FactoryT<std::vector<final_stmt *>> VectorOffinal_stmtFactory;
typedef FactoryT<std::vector<for_stmt *>> VectorOffor_stmtFactory;
typedef FactoryT<std::vector<force *>> VectorOfforceFactory;
typedef FactoryT<std::vector<foreach_stmt *>> VectorOfforeach_stmtFactory;
typedef FactoryT<std::vector<forever_stmt *>> VectorOfforever_stmtFactory;
typedef FactoryT<std::vector<fork_stmt *>> VectorOffork_stmtFactory;
typedef FactoryT<std::vector<func_call *>> VectorOffunc_callFactory;
typedef FactoryT<std::vector<function *>> VectorOffunctionFactory;
typedef FactoryT<std::vector<gate *>> VectorOfgateFactory;
typedef FactoryT<std::vector<gate_array *>> VectorOfgate_arrayFactory;
typedef FactoryT<std::vector<gen_scope *>> VectorOfgen_scopeFactory;
typedef FactoryT<std::vector<gen_scope_array *>> VectorOfgen_scope_arrayFactory;
typedef FactoryT<std::vector<gen_var *>> VectorOfgen_varFactory;
typedef FactoryT<std::vector<hier_path *>> VectorOfhier_pathFactory;
typedef FactoryT<std::vector<if_else *>> VectorOfif_elseFactory;
typedef FactoryT<std::vector<if_stmt *>> VectorOfif_stmtFactory;
typedef FactoryT<std::vector<immediate_assert *>> VectorOfimmediate_assertFactory;
typedef FactoryT<std::vector<immediate_assume *>> VectorOfimmediate_assumeFactory;
typedef FactoryT<std::vector<immediate_cover *>> VectorOfimmediate_coverFactory;
typedef FactoryT<std::vector<implication *>> VectorOfimplicationFactory;
typedef FactoryT<std::vector<import_typespec *>> VectorOfimport_typespecFactory;
typedef FactoryT<std::vector<include_file_info *>> VectorOfinclude_file_infoFactory;
typedef FactoryT<std::vector<indexed_part_select *>> VectorOfindexed_part_selectFactory;
typedef FactoryT<std::vector<initial *>> VectorOfinitialFactory;
typedef FactoryT<std::vector<instance *>> VectorOfinstanceFactory;
typedef FactoryT<std::vector<instance_array *>> VectorOfinstance_arrayFactory;
typedef FactoryT<std::vector<int_typespec *>> VectorOfint_typespecFactory;
typedef FactoryT<std::vector<int_var *>> VectorOfint_varFactory;
typedef FactoryT<std::vector<integer_net *>> VectorOfinteger_netFactory;
typedef FactoryT<std::vector<integer_typespec *>> VectorOfinteger_typespecFactory;
typedef FactoryT<std::vector<integer_var *>> VectorOfinteger_varFactory;
typedef FactoryT<std::vector<interface *>> VectorOfinterfaceFactory;
typedef FactoryT<std::vector<interface_array *>> VectorOfinterface_arrayFactory;
typedef FactoryT<std::vector<interface_tf_decl *>> VectorOfinterface_tf_declFactory;
typedef FactoryT<std::vector<interface_typespec *>> VectorOfinterface_typespecFactory;
typedef FactoryT<std::vector<io_decl *>> VectorOfio_declFactory;
typedef FactoryT<std::vector<let_decl *>> VectorOflet_declFactory;
typedef FactoryT<std::vector<let_expr *>> VectorOflet_exprFactory;
typedef FactoryT<std::vector<logic_net *>> VectorOflogic_netFactory;
typedef FactoryT<std::vector<logic_typespec *>> VectorOflogic_typespecFactory;
typedef FactoryT<std::vector<logic_var *>> VectorOflogic_varFactory;
typedef FactoryT<std::vector<long_int_typespec *>> VectorOflong_int_typespecFactory;
typedef FactoryT<std::vector<long_int_var *>> VectorOflong_int_varFactory;
typedef FactoryT<std::vector<method_func_call *>> VectorOfmethod_func_callFactory;
typedef FactoryT<std::vector<method_task_call *>> VectorOfmethod_task_callFactory;
typedef FactoryT<std::vector<mod_path *>> VectorOfmod_pathFactory;
typedef FactoryT<std::vector<modport *>> VectorOfmodportFactory;
typedef FactoryT<std::vector<module *>> VectorOfmoduleFactory;
typedef FactoryT<std::vector<module_array *>> VectorOfmodule_arrayFactory;
typedef FactoryT<std::vector<module_typespec *>> VectorOfmodule_typespecFactory;
typedef FactoryT<std::vector<multiclock_sequence_expr *>> VectorOfmulticlock_sequence_exprFactory;
typedef FactoryT<std::vector<named_begin *>> VectorOfnamed_beginFactory;
typedef FactoryT<std::vector<named_event *>> VectorOfnamed_eventFactory;
typedef FactoryT<std::vector<named_event_array *>> VectorOfnamed_event_arrayFactory;
typedef FactoryT<std::vector<named_fork *>> VectorOfnamed_forkFactory;
typedef FactoryT<std::vector<net *>> VectorOfnetFactory;
typedef FactoryT<std::vector<net_bit *>> VectorOfnet_bitFactory;
typedef FactoryT<std::vector<net_drivers *>> VectorOfnet_driversFactory;
typedef FactoryT<std::vector<net_loads *>> VectorOfnet_loadsFactory;
typedef FactoryT<std::vector<nets *>> VectorOfnetsFactory;
typedef FactoryT<std::vector<null_stmt *>> VectorOfnull_stmtFactory;
typedef FactoryT<std::vector<operation *>> VectorOfoperationFactory;
typedef FactoryT<std::vector<ordered_wait *>> VectorOfordered_waitFactory;
typedef FactoryT<std::vector<package *>> VectorOfpackageFactory;
typedef FactoryT<std::vector<packed_array_net *>> VectorOfpacked_array_netFactory;
typedef FactoryT<std::vector<packed_array_typespec *>> VectorOfpacked_array_typespecFactory;
typedef FactoryT<std::vector<packed_array_var *>> VectorOfpacked_array_varFactory;
typedef FactoryT<std::vector<param_assign *>> VectorOfparam_assignFactory;
typedef FactoryT<std::vector<parameter *>> VectorOfparameterFactory;
typedef FactoryT<std::vector<part_select *>> VectorOfpart_selectFactory;
typedef FactoryT<std::vector<path_term *>> VectorOfpath_termFactory;
typedef FactoryT<std::vector<port *>> VectorOfportFactory;
typedef FactoryT<std::vector<port_bit *>> VectorOfport_bitFactory;
typedef FactoryT<std::vector<ports *>> VectorOfportsFactory;
typedef FactoryT<std::vector<prim_term *>> VectorOfprim_termFactory;
typedef FactoryT<std::vector<primitive *>> VectorOfprimitiveFactory;
typedef FactoryT<std::vector<primitive_array *>> VectorOfprimitive_arrayFactory;
typedef FactoryT<std::vector<process_stmt *>> VectorOfprocess_stmtFactory;
typedef FactoryT<std::vector<program *>> VectorOfprogramFactory;
typedef FactoryT<std::vector<program_array *>> VectorOfprogram_arrayFactory;
typedef FactoryT<std::vector<prop_formal_decl *>> VectorOfprop_formal_declFactory;
typedef FactoryT<std::vector<property_decl *>> VectorOfproperty_declFactory;
typedef FactoryT<std::vector<property_inst *>> VectorOfproperty_instFactory;
typedef FactoryT<std::vector<property_spec *>> VectorOfproperty_specFactory;
typedef FactoryT<std::vector<property_typespec *>> VectorOfproperty_typespecFactory;
typedef FactoryT<std::vector<range *>> VectorOfrangeFactory;
typedef FactoryT<std::vector<real_typespec *>> VectorOfreal_typespecFactory;
typedef FactoryT<std::vector<real_var *>> VectorOfreal_varFactory;
typedef FactoryT<std::vector<ref_obj *>> VectorOfref_objFactory;
typedef FactoryT<std::vector<ref_var *>> VectorOfref_varFactory;
typedef FactoryT<std::vector<reg *>> VectorOfregFactory;
typedef FactoryT<std::vector<reg_array *>> VectorOfreg_arrayFactory;
typedef FactoryT<std::vector<release *>> VectorOfreleaseFactory;
typedef FactoryT<std::vector<repeat *>> VectorOfrepeatFactory;
typedef FactoryT<std::vector<repeat_control *>> VectorOfrepeat_controlFactory;
typedef FactoryT<std::vector<restrict *>> VectorOfrestrictFactory;
typedef FactoryT<std::vector<return_stmt *>> VectorOfreturn_stmtFactory;
typedef FactoryT<std::vector<scope *>> VectorOfscopeFactory;
typedef FactoryT<std::vector<seq_formal_decl *>> VectorOfseq_formal_declFactory;
typedef FactoryT<std::vector<sequence_decl *>> VectorOfsequence_declFactory;
typedef FactoryT<std::vector<sequence_inst *>> VectorOfsequence_instFactory;
typedef FactoryT<std::vector<sequence_typespec *>> VectorOfsequence_typespecFactory;
typedef FactoryT<std::vector<short_int_typespec *>> VectorOfshort_int_typespecFactory;
typedef FactoryT<std::vector<short_int_var *>> VectorOfshort_int_varFactory;
typedef FactoryT<std::vector<short_real_typespec *>> VectorOfshort_real_typespecFactory;
typedef FactoryT<std::vector<short_real_var *>> VectorOfshort_real_varFactory;
typedef FactoryT<std::vector<simple_expr *>> VectorOfsimple_exprFactory;
typedef FactoryT<std::vector<soft_disable *>> VectorOfsoft_disableFactory;
typedef FactoryT<std::vector<spec_param *>> VectorOfspec_paramFactory;
typedef FactoryT<std::vector<string_typespec *>> VectorOfstring_typespecFactory;
typedef FactoryT<std::vector<string_var *>> VectorOfstring_varFactory;
typedef FactoryT<std::vector<struct_net *>> VectorOfstruct_netFactory;
typedef FactoryT<std::vector<struct_pattern *>> VectorOfstruct_patternFactory;
typedef FactoryT<std::vector<struct_typespec *>> VectorOfstruct_typespecFactory;
typedef FactoryT<std::vector<struct_var *>> VectorOfstruct_varFactory;
typedef FactoryT<std::vector<switch_array *>> VectorOfswitch_arrayFactory;
typedef FactoryT<std::vector<switch_tran *>> VectorOfswitch_tranFactory;
typedef FactoryT<std::vector<sys_func_call *>> VectorOfsys_func_callFactory;
typedef FactoryT<std::vector<sys_task_call *>> VectorOfsys_task_callFactory;
typedef FactoryT<std::vector<table_entry *>> VectorOftable_entryFactory;
typedef FactoryT<std::vector<tagged_pattern *>> VectorOftagged_patternFactory;
typedef FactoryT<std::vector<task *>> VectorOftaskFactory;
typedef FactoryT<std::vector<task_call *>> VectorOftask_callFactory;
typedef FactoryT<std::vector<task_func *>> VectorOftask_funcFactory;
typedef FactoryT<std::vector<tchk *>> VectorOftchkFactory;
typedef FactoryT<std::vector<tchk_term *>> VectorOftchk_termFactory;
typedef FactoryT<std::vector<tf_call *>> VectorOftf_callFactory;
typedef FactoryT<std::vector<thread_obj *>> VectorOfthread_objFactory;
typedef FactoryT<std::vector<time_net *>> VectorOftime_netFactory;
typedef FactoryT<std::vector<time_typespec *>> VectorOftime_typespecFactory;
typedef FactoryT<std::vector<time_var *>> VectorOftime_varFactory;
typedef FactoryT<std::vector<type_parameter *>> VectorOftype_parameterFactory;
typedef FactoryT<std::vector<typespec *>> VectorOftypespecFactory;
typedef FactoryT<std::vector<typespec_member *>> VectorOftypespec_memberFactory;
typedef FactoryT<std::vector<udp *>> VectorOfudpFactory;
typedef FactoryT<std::vector<udp_array *>> VectorOfudp_arrayFactory;
typedef FactoryT<std::vector<udp_defn *>> VectorOfudp_defnFactory;
typedef FactoryT<std::vector<union_typespec *>> VectorOfunion_typespecFactory;
typedef FactoryT<std::vector<union_var *>> VectorOfunion_varFactory;
typedef FactoryT<std::vector<unsupported_expr *>> VectorOfunsupported_exprFactory;
typedef FactoryT<std::vector<unsupported_stmt *>> VectorOfunsupported_stmtFactory;
typedef FactoryT<std::vector<unsupported_typespec *>> VectorOfunsupported_typespecFactory;
typedef FactoryT<std::vector<user_systf *>> VectorOfuser_systfFactory;
typedef FactoryT<std::vector<var_bit *>> VectorOfvar_bitFactory;
typedef FactoryT<std::vector<var_select *>> VectorOfvar_selectFactory;
typedef FactoryT<std::vector<variables *>> VectorOfvariablesFactory;
typedef FactoryT<std::vector<virtual_interface_var *>> VectorOfvirtual_interface_varFactory;
typedef FactoryT<std::vector<void_typespec *>> VectorOfvoid_typespecFactory;
typedef FactoryT<std::vector<wait_fork *>> VectorOfwait_forkFactory;
typedef FactoryT<std::vector<wait_stmt *>> VectorOfwait_stmtFactory;
typedef FactoryT<std::vector<waits *>> VectorOfwaitsFactory;
typedef FactoryT<std::vector<while_stmt *>> VectorOfwhile_stmtFactory;
};


#endif
