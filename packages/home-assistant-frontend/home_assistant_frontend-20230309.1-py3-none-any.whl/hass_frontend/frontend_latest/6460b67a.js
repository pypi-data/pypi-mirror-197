/*! For license information please see 6460b67a.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[25443,76335],{18601:(t,i,e)=>{e.d(i,{Wg:()=>l,qN:()=>r.q});var s,n,o=e(87480),a=e(36924),r=e(78220);const h=null!==(n=null===(s=window.ShadyDOM)||void 0===s?void 0:s.inUse)&&void 0!==n&&n;class l extends r.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=t=>{this.disabled||this.setFormData(t.formData)}}findFormElement(){if(!this.shadowRoot||h)return null;const t=this.getRootNode().querySelectorAll("form");for(const i of Array.from(t))if(i.contains(this))return i;return null}connectedCallback(){var t;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(t=this.containingForm)||void 0===t||t.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this.containingForm)||void 0===t||t.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(t=>{this.dispatchEvent(new Event("change",t))}))}}l.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,o.__decorate)([(0,a.Cb)({type:Boolean})],l.prototype,"disabled",void 0)},14114:(t,i,e)=>{e.d(i,{P:()=>s});const s=t=>(i,e)=>{if(i.constructor._observers){if(!i.constructor.hasOwnProperty("_observers")){const t=i.constructor._observers;i.constructor._observers=new Map,t.forEach(((t,e)=>i.constructor._observers.set(e,t)))}}else{i.constructor._observers=new Map;const t=i.updated;i.updated=function(i){t.call(this,i),i.forEach(((t,i)=>{const e=this.constructor._observers.get(i);void 0!==e&&e.call(this,this[i],t)}))}}i.constructor._observers.set(e,t)}},89833:(t,i,e)=>{e.d(i,{O:()=>c});var s=e(87480),n=e(86251),o=e(37500),a=e(36924),r=e(8636),h=e(51346),l=e(71260);const d={fromAttribute:t=>null!==t&&(""===t||t),toAttribute:t=>"boolean"==typeof t?t?"":null:t};class c extends n.P{constructor(){super(...arguments),this.rows=2,this.cols=20,this.charCounter=!1}render(){const t=this.charCounter&&-1!==this.maxLength,i=t&&"internal"===this.charCounter,e=t&&!i,s=!!this.helper||!!this.validationMessage||e,n={"mdc-text-field--disabled":this.disabled,"mdc-text-field--no-label":!this.label,"mdc-text-field--filled":!this.outlined,"mdc-text-field--outlined":this.outlined,"mdc-text-field--end-aligned":this.endAligned,"mdc-text-field--with-internal-counter":i};return o.dy` <label class="mdc-text-field mdc-text-field--textarea ${(0,r.$)(n)}"> ${this.renderRipple()} ${this.outlined?this.renderOutline():this.renderLabel()} ${this.renderInput()} ${this.renderCharCounter(i)} ${this.renderLineRipple()} </label> ${this.renderHelperText(s,e)} `}renderInput(){const t=this.label?"label":void 0,i=-1===this.minLength?void 0:this.minLength,e=-1===this.maxLength?void 0:this.maxLength,s=this.autocapitalize?this.autocapitalize:void 0;return o.dy` <textarea aria-labelledby="${(0,h.o)(t)}" class="mdc-text-field__input" .value="${(0,l.a)(this.value)}" rows="${this.rows}" cols="${this.cols}" ?disabled="${this.disabled}" placeholder="${this.placeholder}" ?required="${this.required}" ?readonly="${this.readOnly}" minlength="${(0,h.o)(i)}" maxlength="${(0,h.o)(e)}" name="${(0,h.o)(""===this.name?void 0:this.name)}" inputmode="${(0,h.o)(this.inputMode)}" autocapitalize="${(0,h.o)(s)}" @input="${this.handleInputChange}" @blur="${this.onInputBlur}">
      </textarea>`}}(0,s.__decorate)([(0,a.IO)("textarea")],c.prototype,"formElement",void 0),(0,s.__decorate)([(0,a.Cb)({type:Number})],c.prototype,"rows",void 0),(0,s.__decorate)([(0,a.Cb)({type:Number})],c.prototype,"cols",void 0),(0,s.__decorate)([(0,a.Cb)({converter:d})],c.prototype,"charCounter",void 0)},96791:(t,i,e)=>{e.d(i,{W:()=>s});const s=e(37500).iv`.mdc-text-field{height:100%}.mdc-text-field__input{resize:none}`},63207:(t,i,e)=>{e(65660),e(15112);var s=e(9672),n=e(87156),o=e(50856),a=e(48175);(0,s.k)({_template:o.d`
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
`,is:"iron-icon",properties:{icon:{type:String},theme:{type:String},src:{type:String},_meta:{value:a.XY.create("iron-meta",{type:"iconset"})}},observers:["_updateIcon(_meta, isAttached)","_updateIcon(theme, isAttached)","_srcChanged(src, isAttached)","_iconChanged(icon, isAttached)"],_DEFAULT_ICONSET:"icons",_iconChanged:function(t){var i=(t||"").split(":");this._iconName=i.pop(),this._iconsetName=i.pop()||this._DEFAULT_ICONSET,this._updateIcon()},_srcChanged:function(t){this._updateIcon()},_usesIconset:function(){return this.icon||!this.src},_updateIcon:function(){this._usesIconset()?(this._img&&this._img.parentNode&&(0,n.vz)(this.root).removeChild(this._img),""===this._iconName?this._iconset&&this._iconset.removeIcon(this):this._iconsetName&&this._meta&&(this._iconset=this._meta.byKey(this._iconsetName),this._iconset?(this._iconset.applyIcon(this,this._iconName,this.theme),this.unlisten(window,"iron-iconset-added","_updateIcon")):this.listen(window,"iron-iconset-added","_updateIcon"))):(this._iconset&&this._iconset.removeIcon(this),this._img||(this._img=document.createElement("img"),this._img.style.width="100%",this._img.style.height="100%",this._img.draggable=!1),this._img.src=this.src,(0,n.vz)(this.root).appendChild(this._img))}})},15112:(t,i,e)=>{e.d(i,{P:()=>n});e(48175);var s=e(9672);class n{constructor(t){n[" "](t),this.type=t&&t.type||"default",this.key=t&&t.key,t&&"value"in t&&(this.value=t.value)}get value(){var t=this.type,i=this.key;if(t&&i)return n.types[t]&&n.types[t][i]}set value(t){var i=this.type,e=this.key;i&&e&&(i=n.types[i]=n.types[i]||{},null==t?delete i[e]:i[e]=t)}get list(){if(this.type){var t=n.types[this.type];return t?Object.keys(t).map((function(t){return o[this.type][t]}),this):[]}}byKey(t){return this.key=t,this.value}}n[" "]=function(){},n.types={};var o=n.types;(0,s.k)({is:"iron-meta",properties:{type:{type:String,value:"default"},key:{type:String},value:{type:String,notify:!0},self:{type:Boolean,observer:"_selfChanged"},__meta:{type:Boolean,computed:"__computeMeta(type, key, value)"}},hostAttributes:{hidden:!0},__computeMeta:function(t,i,e){var s=new n({type:t,key:i});return void 0!==e&&e!==s.value?s.value=e:this.value!==s.value&&(this.value=s.value),s},get list(){return this.__meta&&this.__meta.list},_selfChanged:function(t){t&&(this.value=this)},byKey:function(t){return new n({type:this.type,key:t}).value}})},54444:(t,i,e)=>{e(48175);var s=e(9672),n=e(87156),o=e(50856);(0,s.k)({_template:o.d`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,n.vz)(this).parentNode,i=(0,n.vz)(this).getOwnerRoot();return this.for?(0,n.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,n.vz)(this).textContent.trim()){for(var t=!0,i=(0,n.vz)(this).getEffectiveChildNodes(),e=0;e<i.length;e++)if(""!==i[e].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,e,s=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),a=(n.width-o.width)/2,r=(n.height-o.height)/2,h=n.left-s.left,l=n.top-s.top;switch(this.position){case"top":i=h+a,e=l-o.height-t;break;case"bottom":i=h+a,e=l+n.height+t;break;case"left":i=h-o.width-t,e=l+r;break;case"right":i=h+n.width+t,e=l+r}this.fitToVisibleBounds?(s.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),s.top+e+o.height>window.innerHeight?(this.style.bottom=s.height-l+t+"px",this.style.top="auto"):(this.style.top=Math.max(-s.top,e)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=e+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},20335:(t,i,e)=>{e.d(i,{e:()=>r});var s=e(73418);function n(t){return"horizontal"===t?"row":"column"}class o extends s.IE{constructor(){super(...arguments),this._itemSize={},this._gaps={},this._padding={}}get _defaultConfig(){return Object.assign({},super._defaultConfig,{itemSize:{width:"300px",height:"300px"},gap:"8px",padding:"match-gap"})}get _gap(){return this._gaps.row}get _idealSize(){return this._itemSize[(0,s.qF)(this.direction)]}get _idealSize1(){return this._itemSize[(0,s.qF)(this.direction)]}get _idealSize2(){return this._itemSize[(0,s.gu)(this.direction)]}get _gap1(){return this._gaps[(t=this.direction,"horizontal"===t?"column":"row")];var t}get _gap2(){return this._gaps[n(this.direction)]}get _padding1(){const t=this._padding,[i,e]="horizontal"===this.direction?["left","right"]:["top","bottom"];return[t[i],t[e]]}get _padding2(){const t=this._padding,[i,e]="horizontal"===this.direction?["top","bottom"]:["left","right"];return[t[i],t[e]]}set itemSize(t){const i=this._itemSize;"string"==typeof t&&(t={width:t,height:t});const e=parseInt(t.width),s=parseInt(t.height);e!==i.width&&(i.width=e,this._triggerReflow()),s!==i.height&&(i.height=s,this._triggerReflow())}set gap(t){const i=t.split(" ").map((t=>function(t){return"auto"===t?1/0:parseInt(t)}(t))),e=this._gaps;i[0]!==e.row&&(e.row=i[0],this._triggerReflow()),void 0===i[1]?i[0]!==e.column&&(e.column=i[0],this._triggerReflow()):i[1]!==e.column&&(e.column=i[1],this._triggerReflow())}set padding(t){const i=this._padding,e=t.split(" ").map((t=>function(t){return"match-gap"===t?1/0:parseInt(t)}(t)));1===e.length?i.top=i.right=i.bottom=i.left=e[0]:2===e.length?(i.top=i.bottom=e[0],i.right=i.left=e[1]):3===e.length?(i.top=e[0],i.right=i.left=e[1],i.bottom=e[2]):4===e.length&&["top","right","bottom","left"].forEach(((t,s)=>i[t]=e[s]))}}class a extends o{constructor(){super(...arguments),this._metrics=null,this.flex=null,this.justify=null}get _defaultConfig(){return Object.assign({},super._defaultConfig,{flex:!1,justify:"start"})}set gap(t){super.gap=t}_updateLayout(){const t=this.justify,[i,e]=this._padding1,[o,a]=this._padding2;["_gap1","_gap2"].forEach((i=>{const e=this[i];if(e===1/0&&!["space-between","space-around","space-evenly"].includes(t))throw new Error("grid layout: gap can only be set to 'auto' when justify is set to 'space-between', 'space-around' or 'space-evenly'");if(e===1/0&&"_gap2"===i)throw new Error(`grid layout: ${n(this.direction)}-gap cannot be set to 'auto' when direction is set to ${this.direction}`)}));const r=this.flex||["start","center","end"].includes(t),h={rolumns:-1,itemSize1:-1,itemSize2:-1,gap1:this._gap1===1/0?-1:this._gap1,gap2:r?this._gap2:0,padding1:{start:i===1/0?this._gap1:i,end:e===1/0?this._gap1:e},padding2:r?{start:o===1/0?this._gap2:o,end:a===1/0?this._gap2:a}:{start:0,end:0},positions:[]},l=this._viewDim2-h.padding2.start-h.padding2.end;if(l<=0)h.rolumns=0;else{const n=r?h.gap2:0;let o,a=0,d=0;if(l>=this._idealSize2&&(a=Math.floor((l-this._idealSize2)/(this._idealSize2+n))+1,d=a*this._idealSize2+(a-1)*n),this.flex){(l-d)/(this._idealSize2+n)>=.5&&(a+=1),h.rolumns=a,h.itemSize2=Math.round((l-n*(a-1))/a);switch(!0===this.flex?"area":this.flex.preserve){case"aspect-ratio":h.itemSize1=Math.round(this._idealSize1/this._idealSize2*h.itemSize2);break;case(0,s.qF)(this.direction):h.itemSize1=Math.round(this._idealSize1);break;default:h.itemSize1=Math.round(this._idealSize1*this._idealSize2/h.itemSize2)}}else h.itemSize1=this._idealSize1,h.itemSize2=this._idealSize2,h.rolumns=a;if(r){const i=h.rolumns*h.itemSize2+(h.rolumns-1)*h.gap2;o=this.flex||"start"===t?h.padding2.start:"end"===t?this._viewDim2-h.padding2.end-i:Math.round(this._viewDim2/2-i/2)}else{const s=l-h.rolumns*h.itemSize2;"space-between"===t?(h.gap2=Math.round(s/(h.rolumns-1)),o=0):"space-around"===t?(h.gap2=Math.round(s/h.rolumns),o=Math.round(h.gap2/2)):(h.gap2=Math.round(s/(h.rolumns+1)),o=h.gap2),this._gap1===1/0&&(h.gap1=h.gap2,i===1/0&&(h.padding1.start=o),e===1/0&&(h.padding1.end=o))}for(let t=0;t<h.rolumns;t++)h.positions.push(o),o+=h.itemSize2+h.gap2}this._metrics=h}}const r=t=>Object.assign({type:h},t);class h extends a{get _delta(){return this._metrics.itemSize1+this._metrics.gap1}_getItemSize(t){return{[this._sizeDim]:this._metrics.itemSize1,[this._secondarySizeDim]:this._metrics.itemSize2}}_getActiveItems(){const t=this._metrics,{rolumns:i}=t;if(0===i)this._first=-1,this._last=-1,this._physicalMin=0,this._physicalMax=0;else{const{padding1:e}=t,s=Math.max(0,this._scrollPosition-this._overhang),n=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang),o=Math.max(0,Math.floor((s-e.start)/this._delta)),a=Math.max(0,Math.ceil((n-e.start)/this._delta));this._first=o*i,this._last=Math.min(a*i-1,this.items.length-1),this._physicalMin=e.start+this._delta*o,this._physicalMax=e.start+this._delta*a}}_getItemPosition(t){const{rolumns:i,padding1:e,positions:n,itemSize1:o,itemSize2:a}=this._metrics;return{[this._positionDim]:e.start+Math.floor(t/i)*this._delta,[this._secondaryPositionDim]:n[t%i],[(0,s.qF)(this.direction)]:o,[(0,s.gu)(this.direction)]:a}}_updateScrollSize(){const{rolumns:t,gap1:i,padding1:e,itemSize1:s}=this._metrics;let n=1;if(t>0){const o=Math.ceil(this.items.length/t);n=e.start+o*s+(o-1)*i+e.end}this._scrollSize=n}}},73418:(t,i,e)=>{let s,n;async function o(){return n||async function(){s=window.EventTarget;try{new s}catch{s=(await e.e(3182).then(e.bind(e,3182))).EventTarget}return n=s}()}function a(t){return"horizontal"===t?"width":"height"}function r(t){return"horizontal"===t?"height":"width"}e.d(i,{IE:()=>h,qF:()=>a,gu:()=>r});class h{constructor(t){this._latestCoords={left:0,top:0},this._direction=null,this._viewportSize={width:0,height:0},this.totalScrollSize={width:0,height:0},this.offsetWithinScroller={left:0,top:0},this._pendingReflow=!1,this._pendingLayoutUpdate=!1,this._pin=null,this._firstVisible=0,this._lastVisible=0,this._eventTargetPromise=o().then((t=>{this._eventTarget=new t})),this._physicalMin=0,this._physicalMax=0,this._first=-1,this._last=-1,this._sizeDim="height",this._secondarySizeDim="width",this._positionDim="top",this._secondaryPositionDim="left",this._scrollPosition=0,this._scrollError=0,this._items=[],this._scrollSize=1,this._overhang=1e3,this._eventTarget=null,Promise.resolve().then((()=>this.config=t||this._defaultConfig))}get _defaultConfig(){return{direction:"vertical"}}set config(t){Object.assign(this,Object.assign({},this._defaultConfig,t))}get config(){return{direction:this.direction}}get items(){return this._items}set items(t){t!==this._items&&(this._items=t,this._scheduleReflow())}get direction(){return this._direction}set direction(t){(t="horizontal"===t?t:"vertical")!==this._direction&&(this._direction=t,this._sizeDim="horizontal"===t?"width":"height",this._secondarySizeDim="horizontal"===t?"height":"width",this._positionDim="horizontal"===t?"left":"top",this._secondaryPositionDim="horizontal"===t?"top":"left",this._triggerReflow())}get viewportSize(){return this._viewportSize}set viewportSize(t){const{_viewDim1:i,_viewDim2:e}=this;Object.assign(this._viewportSize,t),e!==this._viewDim2?this._scheduleLayoutUpdate():i!==this._viewDim1&&this._checkThresholds()}get viewportScroll(){return this._latestCoords}set viewportScroll(t){Object.assign(this._latestCoords,t);const i=this._scrollPosition;this._scrollPosition=this._latestCoords[this._positionDim];Math.abs(i-this._scrollPosition)>=1&&this._updateVisibleIndices({emit:!0}),this._checkThresholds()}reflowIfNeeded(t=!1){(t||this._pendingReflow)&&(this._pendingReflow=!1,this._reflow())}set pin(t){this._pin=t,this._triggerReflow()}get pin(){if(null!==this._pin){const{index:t,block:i}=this._pin;return{index:Math.max(0,Math.min(t,this.items.length-1)),block:i}}return null}_clampScrollPosition(t){return Math.max(-this.offsetWithinScroller[this._positionDim],Math.min(t,this.totalScrollSize[a(this.direction)]-this._viewDim1))}unpin(){null!==this._pin&&(this._emitUnpinned(),this._pin=null)}async dispatchEvent(t){await this._eventTargetPromise,this._eventTarget.dispatchEvent(t)}async addEventListener(t,i,e){await this._eventTargetPromise,this._eventTarget.addEventListener(t,i,e)}async removeEventListener(t,i,e){await this._eventTargetPromise,this._eventTarget.removeEventListener(t,i,e)}_updateLayout(){}get _viewDim1(){return this._viewportSize[this._sizeDim]}get _viewDim2(){return this._viewportSize[this._secondarySizeDim]}_scheduleReflow(){this._pendingReflow=!0}_scheduleLayoutUpdate(){this._pendingLayoutUpdate=!0,this._scheduleReflow()}_triggerReflow(){this._scheduleLayoutUpdate(),Promise.resolve().then((()=>this.reflowIfNeeded()))}_reflow(){this._pendingLayoutUpdate&&(this._updateLayout(),this._pendingLayoutUpdate=!1),this._updateScrollSize(),this._setPositionFromPin(),this._getActiveItems(),this._updateVisibleIndices(),this._emitScrollSize(),this._emitRange(),this._emitChildPositions(),this._emitScrollError()}_setPositionFromPin(){if(null!==this.pin){const t=this._scrollPosition,{index:i,block:e}=this.pin;this._scrollPosition=this._calculateScrollIntoViewPosition({index:i,block:e||"start"})-this.offsetWithinScroller[this._positionDim],this._scrollError=t-this._scrollPosition}}_calculateScrollIntoViewPosition(t){const{block:i}=t,e=Math.min(this.items.length,Math.max(0,t.index)),s=this._getItemPosition(e)[this._positionDim];let n=s;if("start"!==i){const t=this._getItemSize(e)[this._sizeDim];if("center"===i)n=s-.5*this._viewDim1+.5*t;else{const e=s-this._viewDim1+t;if("end"===i)n=e;else{const t=this._scrollPosition;n=Math.abs(t-s)<Math.abs(t-e)?s:e}}}return n+=this.offsetWithinScroller[this._positionDim],this._clampScrollPosition(n)}getScrollIntoViewCoordinates(t){return{[this._positionDim]:this._calculateScrollIntoViewPosition(t)}}_emitUnpinned(){this.dispatchEvent(new CustomEvent("unpinned"))}_emitRange(){const t={first:this._first,last:this._last,firstVisible:this._firstVisible,lastVisible:this._lastVisible};this.dispatchEvent(new CustomEvent("rangechange",{detail:t}))}_emitScrollSize(){const t={[this._sizeDim]:this._scrollSize,[this._secondarySizeDim]:null};this.dispatchEvent(new CustomEvent("scrollsizechange",{detail:t}))}_emitScrollError(){if(this._scrollError){const t={[this._positionDim]:this._scrollError,[this._secondaryPositionDim]:0};this.dispatchEvent(new CustomEvent("scrollerrorchange",{detail:t})),this._scrollError=0}}_emitChildPositions(){if(-1!==this._first&&-1!==this._last){const t=new Map;for(let i=this._first;i<=this._last;i++)t.set(i,this._getItemPosition(i));this.dispatchEvent(new CustomEvent("itempositionchange",{detail:t}))}}get _num(){return-1===this._first||-1===this._last?0:this._last-this._first+1}_checkThresholds(){if(0===this._viewDim1&&this._num>0||null!==this._pin)this._scheduleReflow();else{const t=Math.max(0,this._scrollPosition-this._overhang),i=Math.min(this._scrollSize,this._scrollPosition+this._viewDim1+this._overhang);(this._physicalMin>t||this._physicalMax<i)&&this._scheduleReflow()}}_updateVisibleIndices(t){if(-1===this._first||-1===this._last)return;let i=this._first;for(;i<this._last&&Math.round(this._getItemPosition(i)[this._positionDim]+this._getItemSize(i)[this._sizeDim])<=Math.round(this._scrollPosition);)i++;let e=this._last;for(;e>this._first&&Math.round(this._getItemPosition(e)[this._positionDim])>=Math.round(this._scrollPosition+this._viewDim1);)e--;i===this._firstVisible&&e===this._lastVisible||(this._firstVisible=i,this._lastVisible=e,t&&t.emit&&this._emitRange())}}},82160:(t,i,e)=>{function s(t){return new Promise(((i,e)=>{t.oncomplete=t.onsuccess=()=>i(t.result),t.onabort=t.onerror=()=>e(t.error)}))}function n(t,i){const e=indexedDB.open(t);e.onupgradeneeded=()=>e.result.createObjectStore(i);const n=s(e);return(t,e)=>n.then((s=>e(s.transaction(i,t).objectStore(i))))}let o;function a(){return o||(o=n("keyval-store","keyval")),o}function r(t,i=a()){return i("readonly",(i=>s(i.get(t))))}function h(t,i,e=a()){return e("readwrite",(e=>(e.put(i,t),s(e.transaction))))}function l(t=a()){return t("readwrite",(t=>(t.clear(),s(t.transaction))))}e.d(i,{MT:()=>n,RV:()=>s,U2:()=>r,ZH:()=>l,t8:()=>h})},19596:(t,i,e)=>{e.d(i,{sR:()=>c});var s=e(81563),n=e(38941);const o=(t,i)=>{var e,s;const n=t._$AN;if(void 0===n)return!1;for(const t of n)null===(s=(e=t)._$AO)||void 0===s||s.call(e,i,!1),o(t,i);return!0},a=t=>{let i,e;do{if(void 0===(i=t._$AM))break;e=i._$AN,e.delete(t),t=i}while(0===(null==e?void 0:e.size))},r=t=>{for(let i;i=t._$AM;t=i){let e=i._$AN;if(void 0===e)i._$AN=e=new Set;else if(e.has(t))break;e.add(t),d(i)}};function h(t){void 0!==this._$AN?(a(this),this._$AM=t,r(this)):this._$AM=t}function l(t,i=!1,e=0){const s=this._$AH,n=this._$AN;if(void 0!==n&&0!==n.size)if(i)if(Array.isArray(s))for(let t=e;t<s.length;t++)o(s[t],!1),a(s[t]);else null!=s&&(o(s,!1),a(s));else o(this,t)}const d=t=>{var i,e,s,o;t.type==n.pX.CHILD&&(null!==(i=(s=t)._$AP)&&void 0!==i||(s._$AP=l),null!==(e=(o=t)._$AQ)&&void 0!==e||(o._$AQ=h))};class c extends n.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(t,i,e){super._$AT(t,i,e),r(this),this.isConnected=t._$AU}_$AO(t,i=!0){var e,s;t!==this.isConnected&&(this.isConnected=t,t?null===(e=this.reconnected)||void 0===e||e.call(this):null===(s=this.disconnected)||void 0===s||s.call(this)),i&&(o(this,t),a(this))}setValue(t){if((0,s.OR)(this._$Ct))this._$Ct._$AI(t,this);else{const i=[...this._$Ct._$AH];i[this._$Ci]=t,this._$Ct._$AI(i,this,0)}}disconnected(){}reconnected(){}}},81563:(t,i,e)=>{e.d(i,{E_:()=>u,OR:()=>r,_Y:()=>l,fk:()=>d,hN:()=>a,hl:()=>p,i9:()=>m,pt:()=>o,ws:()=>_});var s=e(15304);const{I:n}=s.Al,o=t=>null===t||"object"!=typeof t&&"function"!=typeof t,a=(t,i)=>void 0===i?void 0!==(null==t?void 0:t._$litType$):(null==t?void 0:t._$litType$)===i,r=t=>void 0===t.strings,h=()=>document.createComment(""),l=(t,i,e)=>{var s;const o=t._$AA.parentNode,a=void 0===i?t._$AB:i._$AA;if(void 0===e){const i=o.insertBefore(h(),a),s=o.insertBefore(h(),a);e=new n(i,s,t,t.options)}else{const i=e._$AB.nextSibling,n=e._$AM,r=n!==t;if(r){let i;null===(s=e._$AQ)||void 0===s||s.call(e,t),e._$AM=t,void 0!==e._$AP&&(i=t._$AU)!==n._$AU&&e._$AP(i)}if(i!==a||r){let t=e._$AA;for(;t!==i;){const i=t.nextSibling;o.insertBefore(t,a),t=i}}}return e},d=(t,i,e=t)=>(t._$AI(i,e),t),c={},p=(t,i=c)=>t._$AH=i,m=t=>t._$AH,_=t=>{var i;null===(i=t._$AP)||void 0===i||i.call(t,!1,!0);let e=t._$AA;const s=t._$AB.nextSibling;for(;e!==s;){const t=e.nextSibling;e.remove(),e=t}},u=t=>{t._$AR()}},22142:(t,i,e)=>{e.d(i,{C:()=>c});var s=e(15304),n=e(81563),o=e(19596);class a{constructor(t){this.Y=t}disconnect(){this.Y=void 0}reconnect(t){this.Y=t}deref(){return this.Y}}class r{constructor(){this.Z=void 0,this.q=void 0}get(){return this.Z}pause(){var t;null!==(t=this.Z)&&void 0!==t||(this.Z=new Promise((t=>this.q=t)))}resume(){var t;null===(t=this.q)||void 0===t||t.call(this),this.Z=this.q=void 0}}var h=e(38941);const l=t=>!(0,n.pt)(t)&&"function"==typeof t.then;class d extends o.sR{constructor(){super(...arguments),this._$Cwt=1073741823,this._$Cyt=[],this._$CK=new a(this),this._$CX=new r}render(...t){var i;return null!==(i=t.find((t=>!l(t))))&&void 0!==i?i:s.Jb}update(t,i){const e=this._$Cyt;let n=e.length;this._$Cyt=i;const o=this._$CK,a=this._$CX;this.isConnected||this.disconnected();for(let t=0;t<i.length&&!(t>this._$Cwt);t++){const s=i[t];if(!l(s))return this._$Cwt=t,s;t<n&&s===e[t]||(this._$Cwt=1073741823,n=0,Promise.resolve(s).then((async t=>{for(;a.get();)await a.get();const i=o.deref();if(void 0!==i){const e=i._$Cyt.indexOf(s);e>-1&&e<i._$Cwt&&(i._$Cwt=e,i.setValue(t))}})))}return s.Jb}disconnected(){this._$CK.disconnect(),this._$CX.pause()}reconnected(){this._$CK.reconnect(this),this._$CX.resume()}}const c=(0,h.XM)(d)}}]);
//# sourceMappingURL=6460b67a.js.map