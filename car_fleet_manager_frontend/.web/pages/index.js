/** @jsxImportSource @emotion/react */


import { Fragment } from "react"
import { Box as RadixThemesBox, Container as RadixThemesContainer, Flex as RadixThemesFlex, Grid as RadixThemesGrid, Heading as RadixThemesHeading, Link as RadixThemesLink, Text as RadixThemesText } from "@radix-ui/themes"
import NextLink from "next/link"
import { Car as LucideCar, CircleHelp as LucideCircleHelp, User as LucideUser } from "lucide-react"
import NextHead from "next/head"
import { jsx } from "@emotion/react"



export default function Component() {
    




  return (
    jsx(
Fragment,
{},
jsx(
RadixThemesBox,
{css:({ ["as"] : "main", ["minHeight"] : "100vh", ["background"] : "gray.50" })},
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
,),),),),),jsx(
RadixThemesContainer,
{css:({ ["padding"] : "16px", ["align"] : "center", ["@media screen and (min-width: 0)"] : ({ ["width"] : "100%" }), ["@media screen and (min-width: 30em)"] : ({ ["width"] : "80%" }), ["@media screen and (min-width: 48em)"] : ({ ["width"] : "60%" }), ["py"] : 8 }),size:"3"},
jsx(
RadixThemesHeading,
{css:({ ["mb"] : 4 }),size:"4"},
"Fleet Dashboard"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["mb"] : 8 })},
"Welcome to the Car Fleet Manager dashboard. Use the navigation to manage vehicles, drivers, and maintenance."
,),jsx(
RadixThemesGrid,
{columns:"3",css:({ ["gap"] : 6, ["width"] : "100%", ["mb"] : 8 })},
jsx(
RadixThemesBox,
{css:({ ["p"] : 4, ["borderRadius"] : "md", ["background"] : "white", ["boxShadow"] : "md", ["align"] : "center" })},
jsx(LucideCar,{css:({ ["color"] : "blue", ["boxSize"] : 6, ["mb"] : 2 })},)
,jsx(
RadixThemesText,
{as:"p",css:({ ["fontWeight"] : "bold" })},
"Total Vehicles"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "2xl", ["color"] : "blue.700" })},
"123"
,),),jsx(
RadixThemesBox,
{css:({ ["p"] : 4, ["borderRadius"] : "md", ["background"] : "white", ["boxShadow"] : "md", ["align"] : "center" })},
jsx(LucideUser,{css:({ ["color"] : "green", ["boxSize"] : 6, ["mb"] : 2 })},)
,jsx(
RadixThemesText,
{as:"p",css:({ ["fontWeight"] : "bold" })},
"Active Drivers"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "2xl", ["color"] : "green.700" })},
"45"
,),),jsx(
RadixThemesBox,
{css:({ ["p"] : 4, ["borderRadius"] : "md", ["background"] : "white", ["boxShadow"] : "md", ["align"] : "center" })},
jsx(LucideCircleHelp,{css:({ ["color"] : "orange", ["boxSize"] : 6, ["mb"] : 2 })},)
,jsx(
RadixThemesText,
{as:"p",css:({ ["fontWeight"] : "bold" })},
"Upcoming Maintenance"
,),jsx(
RadixThemesText,
{as:"p",css:({ ["fontSize"] : "2xl", ["color"] : "orange.700" })},
"7"
,),),),),jsx(
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
"CarFleetManagerFrontend | Index"
,),jsx("meta",{content:"favicon.ico",property:"og:image"},)
,),)
  )
}
