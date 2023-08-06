/*! For license information please see 1dc24181.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[64101,66601,21233],{54444:(t,i,a)=>{a(48175);var e=a(9672),n=a(87156),o=a(50856);(0,e.k)({_template:o.d`
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
`,is:"paper-tooltip",hostAttributes:{role:"tooltip",tabindex:-1},properties:{for:{type:String,observer:"_findTarget"},manualMode:{type:Boolean,value:!1,observer:"_manualModeChanged"},position:{type:String,value:"bottom"},fitToVisibleBounds:{type:Boolean,value:!1},offset:{type:Number,value:14},marginTop:{type:Number,value:14},animationDelay:{type:Number,value:500,observer:"_delayChange"},animationEntry:{type:String,value:""},animationExit:{type:String,value:""},animationConfig:{type:Object,value:function(){return{entry:[{name:"fade-in-animation",node:this,timing:{delay:0}}],exit:[{name:"fade-out-animation",node:this}]}}},_showing:{type:Boolean,value:!1}},listeners:{webkitAnimationEnd:"_onAnimationEnd"},get target(){var t=(0,n.vz)(this).parentNode,i=(0,n.vz)(this).getOwnerRoot();return this.for?(0,n.vz)(i).querySelector("#"+this.for):t.nodeType==Node.DOCUMENT_FRAGMENT_NODE?i.host:t},attached:function(){this._findTarget()},detached:function(){this.manualMode||this._removeListeners()},playAnimation:function(t){"entry"===t?this.show():"exit"===t&&this.hide()},cancelAnimation:function(){this.$.tooltip.classList.add("cancel-animation")},show:function(){if(!this._showing){if(""===(0,n.vz)(this).textContent.trim()){for(var t=!0,i=(0,n.vz)(this).getEffectiveChildNodes(),a=0;a<i.length;a++)if(""!==i[a].textContent.trim()){t=!1;break}if(t)return}this._showing=!0,this.$.tooltip.classList.remove("hidden"),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.updatePosition(),this._animationPlaying=!0,this.$.tooltip.classList.add(this._getAnimationType("entry"))}},hide:function(){if(this._showing){if(this._animationPlaying)return this._showing=!1,void this._cancelAnimation();this._onAnimationFinish(),this._showing=!1,this._animationPlaying=!0}},updatePosition:function(){if(this._target&&this.offsetParent){var t=this.offset;14!=this.marginTop&&14==this.offset&&(t=this.marginTop);var i,a,e=this.offsetParent.getBoundingClientRect(),n=this._target.getBoundingClientRect(),o=this.getBoundingClientRect(),s=(n.width-o.width)/2,r=(n.height-o.height)/2,l=n.left-e.left,p=n.top-e.top;switch(this.position){case"top":i=l+s,a=p-o.height-t;break;case"bottom":i=l+s,a=p+n.height+t;break;case"left":i=l-o.width-t,a=p+r;break;case"right":i=l+n.width+t,a=p+r}this.fitToVisibleBounds?(e.left+i+o.width>window.innerWidth?(this.style.right="0px",this.style.left="auto"):(this.style.left=Math.max(0,i)+"px",this.style.right="auto"),e.top+a+o.height>window.innerHeight?(this.style.bottom=e.height-p+t+"px",this.style.top="auto"):(this.style.top=Math.max(-e.top,a)+"px",this.style.bottom="auto")):(this.style.left=i+"px",this.style.top=a+"px")}},_addListeners:function(){this._target&&(this.listen(this._target,"mouseenter","show"),this.listen(this._target,"focus","show"),this.listen(this._target,"mouseleave","hide"),this.listen(this._target,"blur","hide"),this.listen(this._target,"tap","hide")),this.listen(this.$.tooltip,"animationend","_onAnimationEnd"),this.listen(this,"mouseenter","hide")},_findTarget:function(){this.manualMode||this._removeListeners(),this._target=this.target,this.manualMode||this._addListeners()},_delayChange:function(t){500!==t&&this.updateStyles({"--paper-tooltip-delay-in":t+"ms"})},_manualModeChanged:function(){this.manualMode?this._removeListeners():this._addListeners()},_cancelAnimation:function(){this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add("hidden")},_onAnimationFinish:function(){this._showing&&(this.$.tooltip.classList.remove(this._getAnimationType("entry")),this.$.tooltip.classList.remove("cancel-animation"),this.$.tooltip.classList.add(this._getAnimationType("exit")))},_onAnimationEnd:function(){this._animationPlaying=!1,this._showing||(this.$.tooltip.classList.remove(this._getAnimationType("exit")),this.$.tooltip.classList.add("hidden"))},_getAnimationType:function(t){if("entry"===t&&""!==this.animationEntry)return this.animationEntry;if("exit"===t&&""!==this.animationExit)return this.animationExit;if(this.animationConfig[t]&&"string"==typeof this.animationConfig[t][0].name){if(this.animationConfig[t][0].timing&&this.animationConfig[t][0].timing.delay&&0!==this.animationConfig[t][0].timing.delay){var i=this.animationConfig[t][0].timing.delay;"entry"===t?this.updateStyles({"--paper-tooltip-delay-in":i+"ms"}):"exit"===t&&this.updateStyles({"--paper-tooltip-delay-out":i+"ms"})}return this.animationConfig[t][0].name}},_removeListeners:function(){this._target&&(this.unlisten(this._target,"mouseenter","show"),this.unlisten(this._target,"focus","show"),this.unlisten(this._target,"mouseleave","hide"),this.unlisten(this._target,"blur","hide"),this.unlisten(this._target,"tap","hide")),this.unlisten(this.$.tooltip,"animationend","_onAnimationEnd"),this.unlisten(this,"mouseenter","hide")}})},79021:(t,i,a)=>{a.d(i,{Z:()=>s});var e=a(90394),n=a(34327),o=a(23682);function s(t,i){(0,o.Z)(2,arguments);var a=(0,n.Z)(t),s=(0,e.Z)(i);return isNaN(s)?new Date(NaN):s?(a.setDate(a.getDate()+s),a):a}},59699:(t,i,a)=>{a.d(i,{Z:()=>r});var e=a(90394),n=a(39244),o=a(23682),s=36e5;function r(t,i){(0,o.Z)(2,arguments);var a=(0,e.Z)(i);return(0,n.Z)(t,a*s)}},39244:(t,i,a)=>{a.d(i,{Z:()=>s});var e=a(90394),n=a(34327),o=a(23682);function s(t,i){(0,o.Z)(2,arguments);var a=(0,n.Z)(t).getTime(),s=(0,e.Z)(i);return new Date(a+s)}},32182:(t,i,a)=>{a.d(i,{Z:()=>s});var e=a(90394),n=a(34327),o=a(23682);function s(t,i){(0,o.Z)(2,arguments);var a=(0,n.Z)(t),s=(0,e.Z)(i);if(isNaN(s))return new Date(NaN);if(!s)return a;var r=a.getDate(),l=new Date(a.getTime());return l.setMonth(a.getMonth()+s+1,0),r>=l.getDate()?l:(a.setFullYear(l.getFullYear(),l.getMonth(),r),a)}},93752:(t,i,a)=>{a.d(i,{Z:()=>o});var e=a(34327),n=a(23682);function o(t){(0,n.Z)(1,arguments);var i=(0,e.Z)(t);return i.setHours(23,59,59,999),i}},70390:(t,i,a)=>{a.d(i,{Z:()=>n});var e=a(93752);function n(){return(0,e.Z)(Date.now())}},47538:(t,i,a)=>{function e(){var t=new Date,i=t.getFullYear(),a=t.getMonth(),e=t.getDate(),n=new Date(0);return n.setFullYear(i,a,e-1),n.setHours(23,59,59,999),n}a.d(i,{Z:()=>e})},27088:(t,i,a)=>{a.d(i,{Z:()=>n});var e=a(59429);function n(){return(0,e.Z)(Date.now())}},83008:(t,i,a)=>{function e(){var t=new Date,i=t.getFullYear(),a=t.getMonth(),e=t.getDate(),n=new Date(0);return n.setFullYear(i,a,e-1),n.setHours(0,0,0,0),n}a.d(i,{Z:()=>e})}}]);
//# sourceMappingURL=1dc24181.js.map