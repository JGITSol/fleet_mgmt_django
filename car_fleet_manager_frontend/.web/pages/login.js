/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Heading as RadixThemesHeading, Text as RadixThemesText, TextField as RadixThemesTextField } from "@radix-ui/themes"
import { Root as RadixFormRoot } from "@radix-ui/react-form"
import { EventLoopContext, StateContexts } from "$/utils/context"
import { Event, getRefValue, getRefValues, isNotNullOrUndefined, isTrue } from "$/utils/state"
import { DebounceInput } from "react-debounce-input"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export function Text_ed489dfc48dc4cbcde9caf659cad0323 () {
  
  const reflex___state____state__pages___login____login_state = useContext(StateContexts.reflex___state____state__pages___login____login_state)





  
  return (
    jsx(
RadixThemesText,
{as:"p",css:({ ["color"] : "red.600", ["mb"] : 2 })},
reflex___state____state__pages___login____login_state.error
,)
  )
}

export function Debounceinput_67723ca67f84251b1e3b4c39b2bf9a7d () {
  
  const reflex___state____state__pages___login____login_state = useContext(StateContexts.reflex___state____state__pages___login____login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_change_5129efb6b8385adb0c55521dd67b4670 = useCallback(((_e) => (addEvents([(Event("reflex___state____state.pages___login____login_state.set_password", ({ ["value"] : _e["target"]["value"] }), ({  })))], [_e], ({  })))), [addEvents, Event])



  
  return (
    jsx(DebounceInput,{"aria-label":"Password",css:({ ["mb"] : 4 }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_5129efb6b8385adb0c55521dd67b4670,placeholder:"Password",required:true,type:"password",value:(isNotNullOrUndefined(reflex___state____state__pages___login____login_state.password) ? reflex___state____state__pages___login____login_state.password : "")},)

  )
}

export function Debounceinput_afeabbbf08e48e5a8d6a46d4289f3895 () {
  
  const reflex___state____state__pages___login____login_state = useContext(StateContexts.reflex___state____state__pages___login____login_state)
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_change_75f6cbf1a0698b97f7d22bb05912f1db = useCallback(((_e) => (addEvents([(Event("reflex___state____state.pages___login____login_state.set_username", ({ ["value"] : _e["target"]["value"] }), ({  })))], [_e], ({  })))), [addEvents, Event])



  
  return (
    jsx(DebounceInput,{"aria-label":"Username",css:({ ["mb"] : 2 }),debounceTimeout:300,element:RadixThemesTextField.Root,onChange:on_change_75f6cbf1a0698b97f7d22bb05912f1db,placeholder:"Username",required:true,value:(isNotNullOrUndefined(reflex___state____state__pages___login____login_state.username) ? reflex___state____state__pages___login____login_state.username : "")},)

  )
}

export function Root_2dc2bdc9f5654765ef40bb3714596bda () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);

  
    const handleSubmit_5f4ef4cde8b807424bbd359271a442e0 = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...({  })};

        (((...args) => (addEvents([(Event("reflex___state____state.pages___login____login_state.handle_login", ({  }), ({  })))], args, ({  }))))(ev));

        if (false) {
            $form.reset()
        }
    })
    




  
  return (
    jsx(
RadixFormRoot,
{"aria-label":"Login form",className:"Root ",css:({ ["width"] : "100%" }),onSubmit:handleSubmit_5f4ef4cde8b807424bbd359271a442e0},
jsx(Debounceinput_afeabbbf08e48e5a8d6a46d4289f3895,{},)
,jsx(Debounceinput_67723ca67f84251b1e3b4c39b2bf9a7d,{},)
,jsx(Button_2f1786b1933c70f7118b8f375efd8ff0,{},)
,jsx(Fragment_49da1b3de210b3e98ee43502fca4f0ce,{},)
,)
  )
}

export function Fragment_49da1b3de210b3e98ee43502fca4f0ce () {
  
  const reflex___state____state__pages___login____login_state = useContext(StateContexts.reflex___state____state__pages___login____login_state)





  
  return (
    jsx(
Fragment,
{},
(isTrue(reflex___state____state__pages___login____login_state.error) ? (jsx(
Fragment,
{},
jsx(Text_ed489dfc48dc4cbcde9caf659cad0323,{},)
,)) : (jsx(Fragment,{},)
)),)
  )
}

export function Button_2f1786b1933c70f7118b8f375efd8ff0 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_9366c5fa4e29e1001f56cd4bc93c3abb = useCallback(((...args) => (addEvents([(Event("reflex___state____state.pages___login____login_state.handle_login", ({  }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{color:"blue",css:({ ["width"] : "100%", ["mb"] : 2 }),onClick:on_click_9366c5fa4e29e1001f56cd4bc93c3abb,type:"submit"},
"Login"
,)
  )
}

export default function Component() {
    




  return (
    jsx(
Fragment,
{},
jsx(
RadixThemesBox,
{css:({ ["@media screen and (min-width: 0)"] : ({ ["width"] : "100%" }), ["@media screen and (min-width: 30em)"] : ({ ["width"] : "90%" }), ["@media screen and (min-width: 48em)"] : ({ ["width"] : "400px" }), ["mx"] : "auto", ["mt"] : 16, ["p"] : 8, ["background"] : "white", ["rounded"] : "md", ["shadow"] : "md", ["as"] : "main" })},
jsx(
RadixThemesHeading,
{css:({ ["mb"] : 4 }),size:"4"},
"Login"
,),jsx(Root_2dc2bdc9f5654765ef40bb3714596bda,{},)
,),jsx(
NextHead,
{},
jsx(
"title",
{},
"CarFleetManagerFrontend | Login"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
