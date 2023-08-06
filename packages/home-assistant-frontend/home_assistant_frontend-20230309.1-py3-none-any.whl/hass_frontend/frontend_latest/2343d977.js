/*! For license information please see 2343d977.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[79230,76335],{18601:(t,i,e)=>{e.d(i,{Wg:()=>c,qN:()=>r.q});var n,o,a=e(87480),s=e(36924),r=e(78220);const l=null!==(o=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==o&&o;class c extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const t=this.getRootNode().querySelectorAll("form");for(const i of Array.from(t))if(i.contains(this))return i;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}c.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,a.__decorate)([(0,s.Cb)({type:Boolean})],c.prototype,"disabled",void 0)},14114:(t,i,e)=>{e.d(i,{P:()=>n});const n=t=>(i,e)=>{if(i.constructor._observers){if(!i.constructor.hasOwnProperty("_observers")){const t=i.constructor._observers;i.constructor._observers=new Map,t.forEach(((t,e)=>i.constructor._observers.set(e,t)))}}else{i.constructor._observers=new Map;const t=i.updated;i.updated=function(i){t.call(this,i),i.forEach(((t,i)=>{const e=this.constructor._observers.get(i);void 0!==e&&e.call(this,this[i],t)}))}}i.constructor._observers.set(e,t)}},54444:(t,i,e)=>{e(48175);var n=e(9672),o=e(87156),a=e(50856);(0,n.k)({_template:a.d`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,o.vz)(this).parentNode,i=(0,o.vz)(this).getOwnerRoot();return this.for?(0,o.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,o.vz)(this).textContent.trim()){for(var t=!0,i=(0,o.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,n=this.offsetParent.getBoundingClientRect(),o=this._target.getBoundingClientRect(),a=this.getBoundingClientRect(),s=(o.width-a.width)/2,r=(o.height-a.height)/2,l=o.left-n.left,c=o.top-n.top;switch(this.position){case"top":i=l+s,e=c-a.height-t;break;case"bottom":i=l+s,e=c+o.height+t;break;case"left":i=l-a.width-t,e=c+r;break;case"right":i=l+o.width+t,e=c+r}this.fitToVisibleBounds?(n.left+i+a.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),n.top+e+a.height>window.innerHeight?(this.style.bottom=n.height-c+t+"px",this.style.top="auto"):(this.style.top=Math.max(-n.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},3239:(t,i,e)=>{function n(t){if(!t||"object"!=typeof t)return t;if("[object Date]"==Object.prototype.toString.call(t))return new Date(t.getTime());if(Array.isArray(t))return t.map(n);var i={};return Object.keys(t).forEach((function(e){i[e]=n(t[e])})),i}e.d(i,{Z:()=>n})},93217:(t,i,e)=>{e.d(i,{Ud:()=>d});const n=Symbol("Comlink.proxy"),o=Symbol("Comlink.endpoint"),a=Symbol("Comlink.releaseProxy"),s=Symbol("Comlink.finalizer"),r=Symbol("Comlink.thrown"),l=t=>"object"==typeof t&&null!==t||"function"==typeof t,c=new Map([["proxy",{canHandle:t=>l(t)&&t[n],serialize(t){const{port1:i,port2:e}=new MessageChannel;return p(t,i),[e,[e]]},deserialize:t=>(t.start(),d(t))}],["throw",{canHandle:t=>l(t)&&r in t,serialize({value:t}){let i;return i=t instanceof Error?{isError:!0,value:{message:t.message,name:t.name,stack:t.stack}}:{isError:!1,value:t},[i,[]]},deserialize(t){if(t.isError)throw Object.assign(new Error(t.value.message),t.value);throw t.value}}]]);function p(t,i=globalThis,e=["*"]){i.addEventListener("message",(function o(a){if(!a||!a.data)return;if(!function(t,i){for(const e of t){if(i===e||"*"===e)return!0;if(e instanceof RegExp&&e.test(i))return!0}return!1}(e,a.origin))return void console.warn(`Invalid origin '${a.origin}' for comlink proxy`);const{id:l,type:c,path:d}=Object.assign({path:[]},a.data),m=(a.data.argumentList||[]).map(A);let u;try{const i=d.slice(0,-1).reduce(((t,i)=>t[i]),t),e=d.reduce(((t,i)=>t[i]),t);switch(c){case"GET":u=e;break;case"SET":i[d.slice(-1)[0]]=A(a.data.value),u=!0;break;case"APPLY":u=e.apply(i,m);break;case"CONSTRUCT":u=function(t){return Object.assign(t,{[n]:!0})}(new e(...m));break;case"ENDPOINT":{const{port1:i,port2:e}=new MessageChannel;p(t,e),u=function(t,i){return _.set(t,i),t}(i,[i])}break;case"RELEASE":u=void 0;break;default:return}}catch(t){u={value:t,[r]:0}}Promise.resolve(u).catch((t=>({value:t,[r]:0}))).then((e=>{const[n,a]=b(e);i.postMessage(Object.assign(Object.assign({},n),{id:l}),a),"RELEASE"===c&&(i.removeEventListener("message",o),h(i),s in t&&"function"==typeof t[s]&&t[s]())})).catch((t=>{const[e,n]=b({value:new TypeError("Unserializable return value"),[r]:0});i.postMessage(Object.assign(Object.assign({},e),{id:l}),n)}))})),i.start&&i.start()}function h(t){(function(t){return"MessagePort"===t.constructor.name})(t)&&t.close()}function d(t,i){return g(t,[],i)}function m(t){if(t)throw new Error("Proxy has been released and is not useable")}function u(t){return w(t,{type:"RELEASE"}).then((()=>{h(t)}))}const f=new WeakMap,y="FinalizationRegistry"in globalThis&&new FinalizationRegistry((t=>{const i=(f.get(t)||0)-1;f.set(t,i),0===i&&u(t)}));function g(t,i=[],e=function(){}){let n=!1;const s=new Proxy(e,{get(e,o){if(m(n),o===a)return()=>{!function(t){y&&y.unregister(t)}(s),u(t),n=!0};if("then"===o){if(0===i.length)return{then:()=>s};const e=w(t,{type:"GET",path:i.map((t=>t.toString()))}).then(A);return e.then.bind(e)}return g(t,[...i,o])},set(e,o,a){m(n);const[s,r]=b(a);return w(t,{type:"SET",path:[...i,o].map((t=>t.toString())),value:s},r).then(A)},apply(e,a,s){m(n);const r=i[i.length-1];if(r===o)return w(t,{type:"ENDPOINT"}).then(A);if("bind"===r)return g(t,i.slice(0,-1));const[l,c]=v(s);return w(t,{type:"APPLY",path:i.map((t=>t.toString())),argumentList:l},c).then(A)},construct(e,o){m(n);const[a,s]=v(o);return w(t,{type:"CONSTRUCT",path:i.map((t=>t.toString())),argumentList:a},s).then(A)}});return function(t,i){const e=(f.get(i)||0)+1;f.set(i,e),y&&y.register(t,i,t)}(s,t),s}function v(t){const i=t.map(b);return[i.map((t=>t[0])),(e=i.map((t=>t[1])),Array.prototype.concat.apply([],e))];var e}const _=new WeakMap;function b(t){for(const[i,e]of c)if(e.canHandle(t)){const[n,o]=e.serialize(t);return[{type:"HANDLER",name:i,value:n},o]}return[{type:"RAW",value:t},_.get(t)||[]]}function A(t){switch(t.type){case"HANDLER":return c.get(t.name).deserialize(t.value);case"RAW":return t.value}}function w(t,i,e){return new Promise((n=>{const o=new Array(4).fill(0).map((()=>Math.floor(Math.random()*Number.MAX_SAFE_INTEGER).toString(16))).join("-");t.addEventListener("message",(function i(e){e.data&&e.data.id&&e.data.id===o&&(t.removeEventListener("message",i),n(e.data))})),t.start&&t.start(),t.postMessage(Object.assign({id:o},i),e)}))}},19596:(t,i,e)=>{e.d(i,{sR:()=>h});var n=e(81563),o=e(38941);const a=(t,i)=>{var e,n;const o=t._$AN;if(void 0===o)return!1;for(const t of o)null===(n=(e=t)._$AO)||void 0===n||n.call(e,i,!1),a(t,i);return!0},s=t=>{let i,e;do{if(void 0===(i=t._$AM))break;e=i._$AN,e.delete(t),t=i}while(0===(null==e?void 0:e.size))},r=t=>{for(let i;i=t._$AM;t=i){let e=i._$AN;if(void 0===e)i._$AN=e=new Set;else if(e.has(t))break;e.add(t),p(i)}};function l(t){void 0!==this._$AN?(s(this),this._$AM=t,r(this)):this._$AM=t}function c(t,i=!1,e=0){const n=this._$AH,o=this._$AN;if(void 0!==o&&0!==o.size)if(i)if(Array.isArray(n))for(let t=e;t<n.length;t++)a(n[t],!1),s(n[t]);else null!=n&&(a(n,!1),s(n));else a(this,t)}const p=t=>{var i,e,n,a;t.type==o.pX.CHILD&&(null!==(i=(n=t)._$AP)&&void 0!==i||(n._$AP=c),null!==(e=(a=t)._$AQ)&&void 0!==e||(a._$AQ=l))};class h extends o.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,i,e){super._$AT(t,i,e),r(this),this.isConnected=t._$AU}_$AO(t,i=!0){var e,n;t!==this.isConnected&&(this.isConnected=t,t?null===(e=this.reconnected)||void 0===e||e.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),i&&(a(this,t),s(this))}setValue(t){if((0,n.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const i=[...this._$Ct._$AH];i[this._$Ci]=t,this._$Ct._$AI(i,this,0)}}disconnected(){}reconnected(){}}},81563:(t,i,e)=>{e.d(i,{E_:()=>f,OR:()=>r,_Y:()=>c,fk:()=>p,hN:()=>s,hl:()=>d,i9:()=>m,pt:()=>a,ws:()=>u});var n=e(15304);const{I:o}=n.Al,a=t=>null===t||"object"!=typeof t&&"function"!=typeof t,s=(t,i)=>void 0===i?void 0!==(null==t?void 0:t._$litType$):(null==t?void 0:t._$litType$)===i,r=t=>void 0===t.strings,l=()=>document.createComment(""),c=(t,i,e)=>{var n;const a=t._$AA.parentNode,s=void 0===i?t._$AB:i._$AA;if(void 0===e){const i=a.insertBefore(l(),s),n=a.insertBefore(l(),s);e=new o(i,n,t,t.options)}else{const i=e._$AB.nextSibling,o=e._$AM,r=o!==t;if(r){let i;null===(n=e._$AQ)||void 0===n||n.call(e,t),e._$AM=t,void 0!==e._$AP&&(i=t._$AU)!==o._$AU&&e._$AP(i)}if(i!==s||r){let t=e._$AA;for(;t!==i;){const i=t.nextSibling;a.insertBefore(t,s),t=i}}}return e},p=(t,i,e=t)=>(t._$AI(i,e),t),h={},d=(t,i=h)=>t._$AH=i,m=t=>t._$AH,u=t=>{var i;null===(i=t._$AP)||void 0===i||i.call(t,!1,!0);let e=t._$AA;const n=t._$AB.nextSibling;for(;e!==n;){const t=e.nextSibling;e.remove(),e=t}},f=t=>{t._$AR()}},57835:(t,i,e)=>{e.d(i,{XM:()=>n.XM,Xe:()=>n.Xe,pX:()=>n.pX});var n=e(38941)}}]);
//# sourceMappingURL=2343d977.js.map