/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext } from "react"
import { Box as RadixThemesBox, Button as RadixThemesButton, Container as RadixThemesContainer, Flex as RadixThemesFlex, Heading as RadixThemesHeading, Link as RadixThemesLink, Text as RadixThemesText } from "@radix-ui/themes"
import NextLink from "next/link"
import { EventLoopContext } from "$/utils/context"
import { Event } from "$/utils/state"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export function Button_be77effafb061403eba62e893f6b55b0 () {
  
  const [addEvents, connectErrors] = useContext(EventLoopContext);


  const on_click_20c8b694af07851e42f69c3438fbee1f = useCallback(((...args) => (addEvents([(Event("reflex___state____state.pages___drivers____drivers_state.fetch_drivers", ({  }), ({  })))], args, ({  })))), [addEvents, Event])



  
  return (
    jsx(
RadixThemesButton,
{onClick:on_click_20c8b694af07851e42f69c3438fbee1f},
"Load Drivers"
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
{},
jsx(
RadixThemesBox,
{"aria-label":"Main navigation",css:({ ["background"] : "white", ["shadow"] : "sm", ["as"] : "header" }),role:"navigation"},
jsx(
RadixThemesContainer,
{css:({ ["padding"] : "16px", ["py"] : 4, ["@media screen and (min-width: 0)"] : ({ ["width"] : "100%" }), ["@media screen and (min-width: 30em)"] : ({ ["width"] : "80%" }), ["@media screen and (min-width: 48em)"] : ({ ["width"] : "60%" }) }),size:"3"},
jsx(
RadixThemesFlex,
{align:"start",className:"rx-Stack",direction:"row",gap:"2"},
jsx(
RadixThemesHeading,
{as:"a",css:({ ["color"] : "blue.700", ["href"] : "/", ["mr"] : 8 }),size:"4"},
"Car Fleet Manager"
,),jsx(RadixThemesFlex,{css:({ ["flex"] : 1, ["justifySelf"] : "stretch", ["alignSelf"] : "stretch" })},)
,jsx(
RadixThemesLink,
{asChild:true,css:({ ["px"] : 4, ["py"] : 2, ["rounded"] : "md", ["&:hover"] : ({ ["background"] : "blue.100" }) })},
jsx(
NextLink,
{href:"/",passHref:true},
"Dashboard"
,),),jsx(
RadixThemesLink,
{asChild:true,css:({ ["px"] : 4, ["py"] : 2, ["rounded"] : "md", ["&:hover"] : ({ ["background"] : "blue.100" }) })},
jsx(
NextLink,
{href:"/vehicles",passHref:true},
"Vehicles"
,),),jsx(
RadixThemesLink,
{asChild:true,css:({ ["px"] : 4, ["py"] : 2, ["rounded"] : "md", ["&:hover"] : ({ ["background"] : "blue.100" }) })},
jsx(
NextLink,
{href:"/drivers",passHref:true},
"Drivers"
,),),jsx(
RadixThemesLink,
{asChild:true,css:({ ["px"] : 4, ["py"] : 2, ["rounded"] : "md", ["&:hover"] : ({ ["background"] : "blue.100" }) })},
jsx(
NextLink,
{href:"/maintenance",passHref:true},
"Maintenance"
,),),),),),jsx(Button_be77effafb061403eba62e893f6b55b0,{},)
,jsx(
RadixThemesBox,
{css:({ ["background"] : "white", ["shadow"] : "sm", ["as"] : "footer" }),role:"contentinfo"},
jsx(
RadixThemesContainer,
{css:({ ["padding"] : "16px", ["py"] : 4, ["@media screen and (min-width: 0)"] : ({ ["width"] : "100%" }), ["@media screen and (min-width: 30em)"] : ({ ["width"] : "80%" }), ["@media screen and (min-width: 48em)"] : ({ ["width"] : "60%" }), ["align"] : "center" }),size:"3"},
jsx(
RadixThemesText,
{as:"p",css:({ ["color"] : "gray.600", ["fontSize"] : "sm" })},
"\u00a9 2025 Car Fleet Manager. All rights reserved."
,),),),),jsx(
NextHead,
{},
jsx(
"title",
{},
"CarFleetManagerFrontend | Drivers"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
