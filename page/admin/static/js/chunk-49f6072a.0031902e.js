(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-49f6072a"],{6724:function(t,e,a){"use strict";a("8d41");var i="@@wavesContext";function n(t,e){function a(a){var i=Object.assign({},e.value),n=Object.assign({ele:t,type:"hit",color:"rgba(0, 0, 0, 0.15)"},i),o=n.ele;if(o){o.style.position="relative",o.style.overflow="hidden";var r=o.getBoundingClientRect(),s=o.querySelector(".waves-ripple");switch(s?s.className="waves-ripple":(s=document.createElement("span"),s.className="waves-ripple",s.style.height=s.style.width=Math.max(r.width,r.height)+"px",o.appendChild(s)),n.type){case"center":s.style.top=r.height/2-s.offsetHeight/2+"px",s.style.left=r.width/2-s.offsetWidth/2+"px";break;default:s.style.top=(a.pageY-r.top-s.offsetHeight/2-document.documentElement.scrollTop||document.body.scrollTop)+"px",s.style.left=(a.pageX-r.left-s.offsetWidth/2-document.documentElement.scrollLeft||document.body.scrollLeft)+"px"}return s.style.backgroundColor=n.color,s.className="waves-ripple z-active",!1}}return t[i]?t[i].removeHandle=a:t[i]={removeHandle:a},a}var o={bind:function(t,e){t.addEventListener("click",n(t,e),!1)},update:function(t,e){t.removeEventListener("click",t[i].removeHandle,!1),t.addEventListener("click",n(t,e),!1)},unbind:function(t){t.removeEventListener("click",t[i].removeHandle,!1),t[i]=null,delete t[i]}},r=function(t){t.directive("waves",o)};window.Vue&&(window.waves=o,Vue.use(r)),o.install=r;e["a"]=o},"8d41":function(t,e,a){},9406:function(t,e,a){"use strict";a.r(e);var i=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{staticClass:"app-container"},[a("div",{staticClass:"dashboard-container"},[a("el-row",{staticStyle:{background:"#fff",padding:"16px 16px 0","margin-bottom":"32px","text-align":"center"}},[a("el-date-picker",{attrs:{type:"date","value-format":"yyyy-MM-dd",placeholder:"选择开始日期",align:"right","picker-options":t.pickerOptions},model:{value:t.listQuery.start_time,callback:function(e){t.$set(t.listQuery,"start_time",e)},expression:"listQuery.start_time"}}),a("el-date-picker",{attrs:{type:"date","value-format":"yyyy-MM-dd",placeholder:"选择结束日期",align:"right","picker-options":t.pickerOptions},model:{value:t.listQuery.end_time,callback:function(e){t.$set(t.listQuery,"end_time",e)},expression:"listQuery.end_time"}}),a("el-button",{directives:[{name:"waves",rawName:"v-waves"}],staticClass:"filter-item",attrs:{type:"primary",icon:"el-icon-search"},on:{click:t.getList}},[t._v(" Search ")])],1),a("el-row",{staticStyle:{background:"#fff",padding:"16px 16px 0","margin-bottom":"32px"}},[a("line-chart",{attrs:{chartData:t.lineChartData}})],1)],1)])},n=[],o=a("5530"),r=a("2f62"),s=a("b775");function l(t){return Object(s["a"])({url:"/api/admin/dashboard",method:"post",data:t})}var c=function(){var t=this,e=t.$createElement,a=t._self._c||e;return a("div",{class:t.className,style:{height:t.height,width:t.width}})},d=[],u=a("313e"),p=a.n(u);a("817d");var h={props:{className:{type:String,default:"chart"},width:{type:String,default:"100%"},height:{type:String,default:"350px"},autoResize:{type:Boolean,default:!0},chartData:{type:Object,required:!0}},data:function(){return{chart:null}},watch:{chartData:{deep:!0,handler:function(t){this.setOptions(t)}}},mounted:function(){var t=this;this.$nextTick((function(){t.initChart()}))},beforeDestroy:function(){this.chart&&(this.chart.dispose(),this.chart=null)},methods:{initChart:function(){this.chart=p.a.init(this.$el,"macarons"),this.setOptions(this.chartData)},setOptions:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.incomeData,a=t.paidOrderData,i=t.xAxisData;this.chart.setOption({xAxis:{data:i,boundaryGap:!1,axisTick:{show:!1}},grid:{left:10,right:10,bottom:20,top:30,containLabel:!0},tooltip:{trigger:"axis",axisPointer:{type:"cross"},padding:[5,10]},yAxis:[{type:"value",name:"收入",position:"left",alignTicks:!0,axisLine:{show:!0,lineStyle:{color:"#FF005A"}},axisLabel:{formatter:"{value} $"}},{type:"value",name:"已完成订单数",position:"right",alignTicks:!0,axisLine:{show:!0,lineStyle:{color:"#3888fa"}},axisLabel:{formatter:"{value}"}}],legend:{data:["收入","已完成订单数"]},series:[{name:"收入",itemStyle:{normal:{color:"#FF005A",lineStyle:{color:"#FF005A",width:2}}},yAxisIndex:0,smooth:!0,type:"line",data:e,animationDuration:2800,animationEasing:"cubicInOut"},{name:"已完成订单数",yAxisIndex:1,smooth:!0,type:"line",itemStyle:{normal:{color:"#3888fa",lineStyle:{color:"#3888fa",width:2},areaStyle:{color:"#f3f8ff"}}},data:a,animationDuration:2800,animationEasing:"quadraticOut"}]})}}},m=h,f=a("2877"),y=Object(f["a"])(m,c,d,!1,null,null,null),v=y.exports,g=a("6724"),x={name:"Dashboard",components:{LineChart:v},directives:{waves:g["a"]},created:function(){this.getList()},methods:{getList:function(){var t=this;this.listLoading=!0,l(this.listQuery).then((function(e){var a=e.data.echart_data;t.lineChartData.incomeData=a.income_data,t.lineChartData.paidOrderData=a.paid_order_count_data,t.lineChartData.xAxisData=a.x_axis_data}))}},computed:Object(o["a"])({},Object(r["b"])(["name"])),data:function(){return{listQuery:{start_time:void 0,end_time:void 0},lineChartData:{incomeData:[],paidOrderData:[],xAxisData:[]},pickerOptions:{shortcuts:[{text:"今天",onClick:function(t){t.$emit("pick",new Date)}},{text:"昨天",onClick:function(t){var e=new Date;e.setTime(e.getTime()-864e5),t.$emit("pick",e)}},{text:"一周前",onClick:function(t){var e=new Date;e.setTime(e.getTime()-6048e5),t.$emit("pick",e)}}]}}}},w=x,b=(a("e467"),Object(f["a"])(w,i,n,!1,null,"538999d8",null));e["default"]=b.exports},e467:function(t,e,a){"use strict";a("f7b4")},f7b4:function(t,e,a){}}]);