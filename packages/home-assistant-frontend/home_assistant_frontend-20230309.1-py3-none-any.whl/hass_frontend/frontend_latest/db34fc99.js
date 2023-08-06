/*! For license information please see db34fc99.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[8992,57813,96638,28096,16209],{63207:(t,e,i)=>{i(65660),i(15112);var n=i(9672),a=i(87156),o=i(50856),s=i(48175);(0,n.k)({_template:o.d`
    <style>
      :host {
        @apply --layout-inline;
        @apply --layout-center-center;
        position: relative;

        vertical-align: middle;

        fill: var(--iron-icon-fill-color, currentcolor);
        stroke: var(--iron-icon-stroke-color, none);

        width: var(--iron-icon-width, 24px);
        height: var(--iron-icon-height, 24px);
        @apply --iron-icon;
      }

      :host([hidden]) {
        display: none;
      }
    </style>
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:s.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var e=(t||"").split(":");this._iconName=e.pop(),this._iconsetName=e.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,a.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,a.vz)(this.root).appendChild(this._img))}})},15112:(t,e,i)=>{i.d(e,{P:()=>a});i(48175);var n=i(9672);class a{constructor(t){a[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,e=this.key;if(t&&e)return a.types[t]&&a.types[t][e]}set value(t){var e=this.type,i=this.key;e&&i&&(e=a.types[e]=a.types[e]||{},null==t?delete e[i]:e[i]=t)}get list(){if(this.type){var t=a.types[this.type];return t?Object.keys(t).map((function(t){return o[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}a[" "]=function(){},a.types={};var o=a.types;(0,n.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,e,i){var n=new a({type:t,key:e});return void 0!==i&&i!==n.value?n.value=i:this.value!==n.value&&(this.value=n.value),n},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new a({type:this.type,key:t}).value}})},54444:(t,e,i)=>{i(48175);var n=i(9672),a=i(87156),o=i(50856);(0,n.k)({_template:o.d`
    <style>
      :host {
        display: block;
        position: absolute;
        outline: none;
        z-index: 1002;
        -moz-user-select: none;
        -ms-user-select: none;
        -webkit-user-select: none;
        user-select: none;
        cursor: default;
      }

      #tooltip {
        display: block;
        outline: none;
        @apply --paper-font-common-base;
        font-size: 10px;
        line-height: 1;
        background-color: var(--paper-tooltip-background, #616161);
        color: var(--paper-tooltip-text-color, white);
        padding: 8px;
        border-radius: 2px;
        @apply --paper-tooltip;
      }

      @keyframes keyFrameScaleUp {
        0% {
          transform: scale(0.0);
        }
        100% {
          transform: scale(1.0);
        }
      }

      @keyframes keyFrameScaleDown {
        0% {
          transform: scale(1.0);
        }
        100% {
          transform: scale(0.0);
        }
      }

      @keyframes keyFrameFadeInOpacity {
        0% {
          opacity: 0;
        }
        100% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameFadeOutOpacity {
        0% {
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        100% {
          opacity: 0;
        }
      }

      @keyframes keyFrameSlideDownIn {
        0% {
          transform: translateY(-2000px);
          opacity: 0;
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
      }

      @keyframes keyFrameSlideDownOut {
        0% {
          transform: translateY(0);
          opacity: var(--paper-tooltip-opacity, 0.9);
        }
        10% {
          opacity: 0.2;
        }
        100% {
          transform: translateY(-2000px);
          opacity: 0;
        }
      }

      .fade-in-animation {
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameFadeInOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .fade-out-animation {
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 0ms);
        animation-name: keyFrameFadeOutOpacity;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-up-animation {
        transform: scale(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-in, 500ms);
        animation-name: keyFrameScaleUp;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-in, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .scale-down-animation {
        transform: scale(1);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameScaleDown;
        animation-iteration-count: 1;
        animation-timing-function: ease-in;
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation {
        transform: translateY(-2000px);
        opacity: 0;
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownIn;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.0, 0.0, 0.2, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .slide-down-animation-out {
        transform: translateY(0);
        opacity: var(--paper-tooltip-opacity, 0.9);
        animation-delay: var(--paper-tooltip-delay-out, 500ms);
        animation-name: keyFrameSlideDownOut;
        animation-iteration-count: 1;
        animation-timing-function: cubic-bezier(0.4, 0.0, 1, 1);
        animation-duration: var(--paper-tooltip-duration-out, 500ms);
        animation-fill-mode: forwards;
        @apply --paper-tooltip-animation;
      }

      .cancel-animation {
        animation-delay: -30s !important;
      }

      /* Thanks IE 10. */

      .hidden {
        display: none !important;
      }
    </style>

    <div id="tooltip" class="hidden">
      <slot></slot>
    </div>
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,a.vz)(this).parentNode,e=(0,a.vz)(this).getOwnerRoot();return this.for?(0,a.vz)(e).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?e.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,a.vz)(this).textContent.trim()){for(var t=!0,e=(0,a.vz)(this).getEffectiveChildNodes(),i=0;i<e.length;i++)if(""!==e[i].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var e,i,n=this.offsetParent.getBoundingClientRect(),a=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(a.width-o.width)/2,r=(a.height-o.height)/2,l=a.left-n.left,u=a.top-n.top;switch(this.position){case"top":e=l+s,i=u-o.height-t;break;case"bottom":e=l+s,i=u+a.height+t;break;case"left":e=l-o.width-t,i=u+r;break;case"right":e=l+a.width+t,i=u+r}this.fitToVisibleBounds?(n.left+e+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,e)+"px",this.style.right="auto"),n.top+i+o.height>window.innerHeight?(this.style.bottom=n.height-u+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,i)+"px",this.style.bottom="auto")):(this.style.left=e+"px",this.style.top=i+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var e=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":e+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":e+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},55020:(t,e,i)=>{i.d(e,{j:()=>a});var n={};function a(){return n}},23682:(t,e,i)=>{function n(t,e){if(e.length<t)throw new TypeError(t+" argument"+(t>1?"s":"")+" required, but only "+e.length+" present")}i.d(e,{Z:()=>n})},86102:(t,e,i)=>{i.d(e,{u:()=>o});var n={ceil:Math.ceil,round:Math.round,floor:Math.floor,trunc:function(t){return t<0?Math.ceil(t):Math.floor(t)}},a="trunc";function o(t){return t?n[t]:n[a]}},90394:(t,e,i)=>{function n(t){if(null===t||!0===t||!1===t)return NaN;var e=Number(t);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}i.d(e,{Z:()=>n})},4535:(t,e,i)=>{i.d(e,{Z:()=>u});var n=i(34327);function a(t){var e=new Date(Date.UTC(t.getFullYear(),t.getMonth(),t.getDate(),t.getHours(),t.getMinutes(),t.getSeconds(),t.getMilliseconds()));return e.setUTCFullYear(t.getFullYear()),t.getTime()-e.getTime()}var o=i(59429),s=i(23682),r=864e5;function l(t,e){var i=t.getFullYear()-e.getFullYear()||t.getMonth()-e.getMonth()||t.getDate()-e.getDate()||t.getHours()-e.getHours()||t.getMinutes()-e.getMinutes()||t.getSeconds()-e.getSeconds()||t.getMilliseconds()-e.getMilliseconds();return i<0?-1:i>0?1:i}function u(t,e){(0,s.Z)(2,arguments);var i=(0,n.Z)(t),u=(0,n.Z)(e),p=l(i,u),c=Math.abs(function(t,e){(0,s.Z)(2,arguments);var i=(0,o.Z)(t),n=(0,o.Z)(e),l=i.getTime()-a(i),u=n.getTime()-a(n);return Math.round((l-u)/r)}(i,u));i.setDate(i.getDate()-p*c);var h=p*(c-Number(l(i,u)===-p));return 0===h?0:h}},35040:(t,e,i)=>{i.d(e,{Z:()=>s});var n=i(4535),a=i(23682),o=i(86102);function s(t,e,i){(0,a.Z)(2,arguments);var s=(0,n.Z)(t,e)/7;return(0,o.u)(null==i?void 0:i.roundingMethod)(s)}},59429:(t,e,i)=>{i.d(e,{Z:()=>o});var n=i(34327),a=i(23682);function o(t){(0,a.Z)(1,arguments);var e=(0,n.Z)(t);return e.setHours(0,0,0,0),e}},59401:(t,e,i)=>{i.d(e,{Z:()=>r});var n=i(34327),a=i(90394),o=i(23682),s=i(55020);function r(t,e){var i,r,l,u,p,c,h,m;(0,o.Z)(1,arguments);var d=(0,s.j)(),y=(0,a.Z)(null!==(i=null!==(r=null!==(l=null!==(u=null==e?void 0:e.weekStartsOn)&&void 0!==u?u:null==e||null===(p=e.locale)||void 0===p||null===(c=p.options)||void 0===c?void 0:c.weekStartsOn)&&void 0!==l?l:d.weekStartsOn)&&void 0!==r?r:null===(h=d.locale)||void 0===h||null===(m=h.options)||void 0===m?void 0:m.weekStartsOn)&&void 0!==i?i:0);if(!(y>=0&&y<=6))throw new RangeError("weekStartsOn must be between 0 and 6 inclusively");var f=(0,n.Z)(t),g=f.getDay(),v=(g<y?7:0)+g-y;return f.setDate(f.getDate()-v),f.setHours(0,0,0,0),f}},34327:(t,e,i)=>{i.d(e,{Z:()=>o});var n=i(23682);function a(t){return a="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"==typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},a(t)}function o(t){(0,n.Z)(1,arguments);var e=Object.prototype.toString.call(t);return t instanceof Date||"object"===a(t)&&"[object Date]"===e?new Date(t.getTime()):"number"==typeof t||"[object Number]"===e?new Date(t):("string"!=typeof t&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://github.com/date-fns/date-fns/blob/master/docs/upgradeGuide.md#string-arguments"),console.warn((new Error).stack)),new Date(NaN))}},95337:(t,e,i)=>{i.d(e,{L:()=>o});const n={en:"US",hi:"IN",deva:"IN",te:"IN",mr:"IN",ta:"IN",gu:"IN",kn:"IN",or:"IN",ml:"IN",pa:"IN",bho:"IN",awa:"IN",as:"IN",mwr:"IN",mai:"IN",mag:"IN",bgc:"IN",hne:"IN",dcc:"IN",bn:"BD",beng:"BD",rkt:"BD",dz:"BT",tibt:"BT",tn:"BW",am:"ET",ethi:"ET",om:"ET",quc:"GT",id:"ID",jv:"ID",su:"ID",mad:"ID",ms_arab:"ID",he:"IL",hebr:"IL",jam:"JM",ja:"JP",jpan:"JP",km:"KH",khmr:"KH",ko:"KR",kore:"KR",lo:"LA",laoo:"LA",mh:"MH",my:"MM",mymr:"MM",mt:"MT",ne:"NP",fil:"PH",ceb:"PH",ilo:"PH",ur:"PK",pa_arab:"PK",lah:"PK",ps:"PK",sd:"PK",skr:"PK",gn:"PY",th:"TH",thai:"TH",tts:"TH",zh_hant:"TW",hant:"TW",sm:"WS",zu:"ZA",sn:"ZW",arq:"DZ",ar:"EG",arab:"EG",arz:"EG",fa:"IR",az_arab:"IR",dv:"MV",thaa:"MV"};const a={AG:0,ATG:0,28:0,AS:0,ASM:0,16:0,BD:0,BGD:0,50:0,BR:0,BRA:0,76:0,BS:0,BHS:0,44:0,BT:0,BTN:0,64:0,BW:0,BWA:0,72:0,BZ:0,BLZ:0,84:0,CA:0,CAN:0,124:0,CO:0,COL:0,170:0,DM:0,DMA:0,212:0,DO:0,DOM:0,214:0,ET:0,ETH:0,231:0,GT:0,GTM:0,320:0,GU:0,GUM:0,316:0,HK:0,HKG:0,344:0,HN:0,HND:0,340:0,ID:0,IDN:0,360:0,IL:0,ISR:0,376:0,IN:0,IND:0,356:0,JM:0,JAM:0,388:0,JP:0,JPN:0,392:0,KE:0,KEN:0,404:0,KH:0,KHM:0,116:0,KR:0,KOR:0,410:0,LA:0,LA0:0,418:0,MH:0,MHL:0,584:0,MM:0,MMR:0,104:0,MO:0,MAC:0,446:0,MT:0,MLT:0,470:0,MX:0,MEX:0,484:0,MZ:0,MOZ:0,508:0,NI:0,NIC:0,558:0,NP:0,NPL:0,524:0,PA:0,PAN:0,591:0,PE:0,PER:0,604:0,PH:0,PHL:0,608:0,PK:0,PAK:0,586:0,PR:0,PRI:0,630:0,PT:0,PRT:0,620:0,PY:0,PRY:0,600:0,SA:0,SAU:0,682:0,SG:0,SGP:0,702:0,SV:0,SLV:0,222:0,TH:0,THA:0,764:0,TT:0,TTO:0,780:0,TW:0,TWN:0,158:0,UM:0,UMI:0,581:0,US:0,USA:0,840:0,VE:0,VEN:0,862:0,VI:0,VIR:0,850:0,WS:0,WSM:0,882:0,YE:0,YEM:0,887:0,ZA:0,ZAF:0,710:0,ZW:0,ZWE:0,716:0,AE:6,ARE:6,784:6,AF:6,AFG:6,4:6,BH:6,BHR:6,48:6,DJ:6,DJI:6,262:6,DZ:6,DZA:6,12:6,EG:6,EGY:6,818:6,IQ:6,IRQ:6,368:6,IR:6,IRN:6,364:6,JO:6,JOR:6,400:6,KW:6,KWT:6,414:6,LY:6,LBY:6,434:6,OM:6,OMN:6,512:6,QA:6,QAT:6,634:6,SD:6,SDN:6,729:6,SY:6,SYR:6,760:6,MV:5,MDV:5,462:5};function o(t){return function(t,e,i){if(t){var n,a=t.toLowerCase().split(/[-_]/),o=a[0],s=o;if(a[1]&&4===a[1].length?(s+="_"+a[1],n=a[2]):n=a[1],n||(n=e[s]||e[o]),n)return function(t,e){var i=e["string"==typeof t?t.toUpperCase():t];return"number"==typeof i?i:1}(n.match(/^\d+$/)?Number(n):n,i)}return 1}(t,n,a)}},93217:(t,e,i)=>{i.d(e,{Ud:()=>h});const n=Symbol("Comlink.proxy"),a=Symbol("Comlink.endpoint"),o=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.finalizer"),r=Symbol("Comlink.thrown"),l=t=>"object"==typeof t&&null!==t||"function"==typeof t,u=new Map([["proxy",{canHandle:t=>l(t)&&t[n],serialize(t){const{port1:e,port2:i}=new MessageChannel;return p(t,e),[i,[i]]},deserialize:t=>(t.start(),h(t))}],["throw",{canHandle:t=>l(t)&&r in t,serialize({value:t}){let e;return e=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[e,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function p(t,e=globalThis,i=["*"]){e.addEventListener("message",(function a(o){if(!o||!o.data)return;if(!function(t,e){for(const i of t){if(e===i||"*"===i)return!0;if(i instanceof RegExp&&i.test(e))return!0}return!1}(i,o.origin))return void console.warn(`Invalid origin '${o.origin}' for comlink proxy`);const{id:l,type:u,path:h}=Object.assign({path:[]},o.data),m=(o.data.argumentList||[]).map(w);let d;try{const e=h.slice(0,-1).reduce(((t,e)=>t[e]),t),i=h.reduce(((t,e)=>t[e]),t);switch(u){case"GET":d=i;break;case"SET":e[h.slice(-1)[0]]=w(o.data.value),d=!0;break;case"APPLY":d=i.apply(e,m);break;case"CONSTRUCT":d=function(t){return Object.assign(t,{[n]:!0})}(new i(...m));break;case"ENDPOINT":{const{port1:e,port2:i}=new MessageChannel;p(t,i),d=function(t,e){return _.set(t,e),t}(e,[e])}break;case"RELEASE":d=void 0;break;default:return}}catch(t){d={value:t,[r]:0}}Promise.resolve(d).catch((t=>({value:t,[r]:0}))).then((i=>{const[n,o]=b(i);e.postMessage(Object.assign(Object.assign({},n),{id:l}),o),"RELEASE"===u&&(e.removeEventListener("message",a),c(e),s in t&&"function"==typeof t[s]&&t[s]())})).catch((t=>{const[i,n]=b({value:new TypeError("Unserializable return value"),[r]:0});e.postMessage(Object.assign(Object.assign({},i),{id:l}),n)}))})),e.start&&e.start()}function c(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function h(t,e){return g(t,[],e)}function m(t){if(t)throw new Error("Proxy has been released and is not useable")}function d(t){return M(t,{type:"RELEASE"}).then((()=>{c(t)}))}const y=new WeakMap,f="FinalizationRegistry"in globalThis&&new FinalizationRegistry((t=>{const e=(y.get(t)||0)-1;y.set(t,e),0===e&&d(t)}));function g(t,e=[],i=function(){}){let n=!1;const s=new Proxy(i,{get(i,a){if(m(n),a===o)return()=>{!function(t){f&&f.unregister(t)}(s),d(t),n=!0};if("then"===a){if(0===e.length)return{then:()=>s};const i=M(t,{type:"GET",path:e.map((t=>t.toString()))}).then(w);return i.then.bind(i)}return g(t,[...e,a])},set(i,a,o){m(n);const[s,r]=b(o);return M(t,{type:"SET",path:[...e,a].map((t=>t.toString())),value:s},r).then(w)},apply(i,o,s){m(n);const r=e[e.length-1];if(r===a)return M(t,{type:"ENDPOINT"}).then(w);if("bind"===r)return g(t,e.slice(0,-1));const[l,u]=v(s);return M(t,{type:"APPLY",path:e.map((t=>t.toString())),argumentList:l},u).then(w)},construct(i,a){m(n);const[o,s]=v(a);return M(t,{type:"CONSTRUCT",path:e.map((t=>t.toString())),argumentList:o},s).then(w)}});return function(t,e){const i=(y.get(e)||0)+1;y.set(e,i),f&&f.register(t,e,t)}(s,t),s}function v(t){const e=t.map(b);return[e.map((t=>t[0])),(i=e.map((t=>t[1])),Array.prototype.concat.apply([],i))];var i}const _=new WeakMap;function b(t){for(const[e,i]of u)if(i.canHandle(t)){const[n,a]=i.serialize(t);return[{type:"HANDLER",name:e,value:n},a]}return[{type:"RAW",value:t},_.get(t)||[]]}function w(t){switch(t.type){case"HANDLER":return u.get(t.name).deserialize(t.value);case"RAW":return t.value}}function M(t,e,i){return new Promise((n=>{const a=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function e(i){i.data&&i.data.id&&i.data.id===a&&(t.removeEventListener("message",e),n(i.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:a},e),i)}))}},82160:(t,e,i)=>{function n(t){return new Promise(((e,i)=>{t.oncomplete=t.onsuccess=()=>e(t.result),t.onabort=t.onerror=()=>i(t.error)}))}function a(t,e){const i=indexedDB.open(t);i.onupgradeneeded=()=>i.result.createObjectStore(e);const a=n(i);return(t,i)=>a.then((n=>i(n.transaction(e,t).objectStore(e))))}let o;function s(){return o||(o=a("keyval-store","keyval")),o}function r(t,e=s()){return e("readonly",(e=>n(e.get(t))))}function l(t,e,i=s()){return i("readwrite",(i=>(i.put(e,t),n(i.transaction))))}function u(t=s()){return t("readwrite",(t=>(t.clear(),n(t.transaction))))}i.d(e,{MT:()=>a,RV:()=>n,U2:()=>r,ZH:()=>u,t8:()=>l})}}]);
//# sourceMappingURL=db34fc99.js.map