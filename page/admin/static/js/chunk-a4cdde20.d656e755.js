(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-a4cdde20"],{"4e82":function(e,t,i){"use strict";var a=i("23e7"),r=i("1c0b"),n=i("7b0b"),l=i("d039"),s=i("a640"),o=[],u=o.sort,c=l((function(){o.sort(void 0)})),d=l((function(){o.sort(null)})),f=s("sort"),p=c||!d||!f;a({target:"Array",proto:!0,forced:p},{sort:function(e){return void 0===e?u.call(n(this)):u.call(n(this),r(e))}})},"634a":function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"app-container"},[i("div",{staticClass:"filter-container"},[i("el-input",{staticClass:"filter-item",staticStyle:{width:"200px"},attrs:{placeholder:"商户ID"},nativeOn:{keyup:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:e.handleFilter(t)}},model:{value:e.listQuery.merchant_id,callback:function(t){e.$set(e.listQuery,"merchant_id",t)},expression:"listQuery.merchant_id"}}),i("el-select",{staticClass:"filter-item",staticStyle:{width:"140px"},on:{change:e.handleFilter},model:{value:e.listQuery.sort,callback:function(t){e.$set(e.listQuery,"sort",t)},expression:"listQuery.sort"}},e._l(e.sortOptions,(function(e){return i("el-option",{key:e.key,attrs:{label:e.label,value:e.key}})})),1),i("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择开始日期",align:"right","picker-options":e.pickerOptions},model:{value:e.listQuery.start_time,callback:function(t){e.$set(e.listQuery,"start_time",t)},expression:"listQuery.start_time"}}),i("el-date-picker",{attrs:{type:"datetime","value-format":"yyyy-MM-dd HH:mm:ss",placeholder:"选择结束日期",align:"right","picker-options":e.pickerOptions},model:{value:e.listQuery.end_time,callback:function(t){e.$set(e.listQuery,"end_time",t)},expression:"listQuery.end_time"}}),i("el-button",{directives:[{name:"waves",rawName:"v-waves"}],staticClass:"filter-item",attrs:{type:"primary",icon:"el-icon-search"},on:{click:e.handleFilter}},[e._v(" 搜索 ")]),i("el-button",{directives:[{name:"waves",rawName:"v-waves"}],staticClass:"filter-item",attrs:{type:"success",icon:"el-icon-plus"},on:{click:function(t){e.dialogGenerateOrderUrlVisible=!0}}},[e._v(" 生成订单链接 ")])],1),i("el-table",{directives:[{name:"loading",rawName:"v-loading",value:e.listLoading,expression:"listLoading"}],key:e.tableKey,staticStyle:{width:"100%"},attrs:{data:e.list,border:"",fit:"","highlight-current-row":""},on:{"sort-change":e.sortChange}},[i("el-table-column",{attrs:{label:"ID",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(a.id))])]}}])}),i("el-table-column",{attrs:{label:"创建时间",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(e._f("parseTime")(1e3*a.create_time,"{y}-{m}-{d} {h}:{i}:{s}")))])]}}])}),i("el-table-column",{attrs:{label:"Status","class-name":"status-col",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("el-tag",{attrs:{type:e._f("statusFilter")(a.status)}},[e._v(" "+e._s(e._f("statusValueFilter")(a.status))+" ")])]}}])}),i("el-table-column",{attrs:{label:"应付金额",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(a.price))])]}}])}),i("el-table-column",{attrs:{label:"已付金额",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(a.paid_price))])]}}])}),i("el-table-column",{attrs:{label:"商户ID",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(a.merchant_id))])]}}])}),i("el-table-column",{attrs:{label:"对应钱包",align:"center"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;return[i("span",[e._v(e._s(a.wallet_id))])]}}])}),i("el-table-column",{attrs:{label:"操作",align:"center",width:"230","class-name":"small-padding fixed-width"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.row;t.$index;return[i("el-button",{attrs:{size:"mini"},on:{click:function(t){return e.handleDetail(a)}}},[e._v(" 详细 ")]),i("el-button",{attrs:{size:"mini",type:"success"},on:{click:function(t){return e.handleNotify(a)}}},[e._v("回调")])]}}])})],1),i("pagination",{directives:[{name:"show",rawName:"v-show",value:e.total>0,expression:"total > 0"}],attrs:{total:e.total,page:e.listQuery.page,limit:e.listQuery.limit},on:{"update:page":function(t){return e.$set(e.listQuery,"page",t)},"update:limit":function(t){return e.$set(e.listQuery,"limit",t)},pagination:e.getList}}),i("el-dialog",{attrs:{visible:e.dialogOrderDetailVisible,title:"Order details"},on:{"update:visible":function(t){e.dialogOrderDetailVisible=t}}},[i("el-form",{attrs:{size:"mini"}},e._l(e.orderData,(function(t,a,r){return i("el-form-item",{attrs:{label:a}},[i("span",[e._v(e._s(t))])])})),1),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{attrs:{type:"primary"},on:{click:function(t){e.dialogOrderDetailVisible=!1}}},[e._v("Confirm")])],1)],1),i("el-dialog",{attrs:{visible:e.dialogGenerateOrderUrlVisible,title:"生成订单链接"},on:{"update:visible":function(t){e.dialogGenerateOrderUrlVisible=t}}},[i("el-container",[i("el-main",[i("el-select",{attrs:{placeholder:"请选择"},model:{value:e.generateOrderQuery.notify_type,callback:function(t){e.$set(e.generateOrderQuery,"notify_type",t)},expression:"generateOrderQuery.notify_type"}},e._l(e.generateOrderNotifyOptions,(function(e){return i("el-option",{key:e.value,attrs:{label:e.label,value:e.value}})})),1)],1),i("el-footer",[i("el-button",{attrs:{type:"primary"},on:{click:e.handleGenerateOrderUrl}},[e._v(" 生成订单链接 ")])],1)],1)],1)],1)},r=[],n=(i("d81d"),i("b0c0"),i("4e82"),i("7db0"),i("d3b7"),i("b775"));function l(e){return Object(n["a"])({url:"/api/admin/order",method:"post",data:e})}function s(e){return Object(n["a"])({url:"/api/admin/order_notify",method:"post",data:e})}function o(e){return Object(n["a"])({url:"/api/admin/order_url_generate",method:"post",data:e})}var u=i("6724"),c=i("ed08"),d=i("333d"),f=(i("a78e"),{name:"Order",components:{Pagination:d["a"]},directives:{waves:u["a"]},filters:{statusFilter:function(e){var t={1:"success",0:"info","-1":"danger"};return t[e]},statusValueFilter:function(e){var t={1:"成功",0:"待支付","-1":"超时"};return t[e]},typeFilter:function(e){return calendarTypeKeyValue[e]},parseTime:c["a"]},data:function(){return{test_var:"",tableKey:0,list:null,total:0,dialogGenerateOrderUrlVisible:!1,generateOrderNotifyOptions:[],generateOrderQuery:{notify_type:""},listLoading:!0,listQuery:{page:1,limit:20,start_time:void 0,end_time:void 0,merchant_id:void 0,sort:"desc"},sortOptions:[{label:"ID 升序",key:"asc"},{label:"ID 降序",key:"desc"}],dialogOrderDetailVisible:!1,orderData:{},rules:{type:[{required:!0,message:"type is required",trigger:"change"}],timestamp:[{type:"date",required:!0,message:"timestamp is required",trigger:"change"}],title:[{required:!0,message:"title is required",trigger:"blur"}]},pickerOptions:{shortcuts:[{text:"今天",onClick:function(e){e.$emit("pick",new Date)}},{text:"昨天",onClick:function(e){var t=new Date;t.setTime(t.getTime()-864e5),e.$emit("pick",t)}},{text:"一周前",onClick:function(e){var t=new Date;t.setTime(t.getTime()-6048e5),e.$emit("pick",t)}}]}}},created:function(){this.getList()},methods:{getList:function(){var e=this;this.listLoading=!0,l(this.listQuery).then((function(t){e.list=t.data.items,e.total=t.data.total,e.generateOrderNotifyOptions=t.data.order_notify_types.map((function(e){return{value:e.key,label:e.name}})),e.listLoading=!1}))},handleFilter:function(){this.listQuery.page=1,this.getList()},handleModifyStatus:function(e,t){this.$message({message:"操作Success",type:"success"}),e.status=t},sortChange:function(e){var t=e.prop,i=e.order;"id"===t&&this.sortByID(i)},sortByID:function(e){this.listQuery.sort="ascending"===e?"acs":"decs",this.handleFilter()},handleDetail:function(e){var t=this.list.find((function(t){return t.id==e.id}));this.dialogOrderDetailVisible=!0,this.orderData=t},handleNotify:function(e){var t=this,i=e.id;s({id:i}).then((function(e){t.$message("回调成功")})).catch((function(e){t.$message("回调失败")}))},handleGenerateOrderUrl:function(){o(this.generateOrderQuery).then((function(e){window.open(e.data,"_blank")}))},test:function(e){console.log(e)}}}),p=f,m=i("2877"),y=Object(m["a"])(p,a,r,!1,null,null,null);t["default"]=y.exports},"7db0":function(e,t,i){"use strict";var a=i("23e7"),r=i("b727").find,n=i("44d2"),l=i("ae40"),s="find",o=!0,u=l(s);s in[]&&Array(1)[s]((function(){o=!1})),a({target:"Array",proto:!0,forced:o||!u},{find:function(e){return r(this,e,arguments.length>1?arguments[1]:void 0)}}),n(s)}}]);