#!/bin/bash
#
# Last Updated: 
# ----------------------------------------------------------------------------------------------------
# Demo for RD32-RS
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# D e f a u l t s
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

default_demo_slot_cfg=9

# ----------------------------------------------------------------------------------------------------

function demo_default_slot {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	[[ -z $1 ]] && \
		echo -e && \
		echo -e " --> Default slot for demo is: ${default_demo_slot_cfg}" && \
		echo -e && \
		return 0

	if [[ ${1} =~ [^[:digit:]] ]] || \
		[[ ${1} -lt 1 ]] || \
		[[ ${1} -gt 20 ]] ; then

		echo -e "\n  Invalid default slot specified (${1})! Expecting 1..20" && \
		return 1
	fi

	default_demo_slot_cfg=${1}
	return 0
}


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# C a r d   &   S l o t
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_showslot {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	local locSlotId_showSlot=$1

	[[ ${locSlotId_showSlot:-unspecified} = unspecified ]] && locSlotId_showSlot=${default_demo_slot_cfg}

    restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_showSlot}"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_showeq {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	local locSlotId_showEq=$1

	[[ ${locSlotId_showEq:-unspecified} = unspecified ]] && locSlotId_showEq=${default_demo_slot_cfg}

    restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_showEq}/eq"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_showcard {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	local locSlotId_showCard=$1

	[[ ${locSlotId_showCard:-unspecified} = unspecified ]] && locSlotId_showCard=${default_demo_slot_cfg}

    restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_showCard}/eq/card"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_addcard {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	local locSlotId_addCard=$1

	[[ ${locSlotId_addCard:-unspecified} = unspecified ]] && locSlotId_addCard=${default_demo_slot_cfg}

	echo -e
	echo -e "-------------------------------------"
	echo -e "--> creating RD-32RS card in slot ${locSlotId_addCard}"
	echo -e "-------------------------------------"

    restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_addCard}/eq/card" '{"card": {"type": "rd32rs"}}'
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_deletecard {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>]${NC}" && \
		return 0

	local locSlotId_delCard=$1

	[[ ${locSlotId_delCard:-unspecified} = unspecified ]] && locSlotId_delCard=${default_demo_slot_cfg}

	echo -e
	echo -e "---------------------------------------------"
	echo -e "--> setting RD-32RS card in slot ${locSlotId_delCard} to OOS"
	echo -e "---------------------------------------------"

    restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_delCard}/eq/card/sm" \
		'[{"op": "replace", "path": "/admin", "value": "oos"}]'

	echo -e "-------------------------------------"
	echo -e "--> deleting RD-32RS card in slot ${locSlotId_delCard}"
	echo -e "-------------------------------------"

    restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_delCard}/eq/card"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# P o r t s
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# return 0 - no errors
# return 1 - invalid port type
# return 2 - invalid port Id
function command_port {

	local locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}$2 [<slotId>] [n1|n2|c1..c33]${NC}"

	[[ "$1" = "?" ]] && \
		echo -e "${locSyntax}" && \
		return 0

	local locPortCmd=$2
	local locSlotId_element=$3
	local locPort_element=$4
	
	[[ ${locSlotId_element:-unspecified} = unspecified ]] && locSlotId_element=${default_demo_slot_cfg}
	[[ ${locPort_element:-unspecified} = unspecified ]] && locPort_element="n1"

	local locPortType=${locPort_element//[^a-zA-Z]/}
	local locPortId=${locPort_element//[^0-9]/}

	local locPortGroupFragment
	local locPortFragment

	if [[ ${locPortType:-unspecified} == "n" ]] ; then

		[[ ${locPortId:-unspecified} -ne 1 ]] && \
			[[ ${locPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locPortFragment="nw,${locPortId}"

	elif [[ ${locPortType:-unspecified} == "c" ]] ; then

		if [[ ${locPortId} -lt 1 ]] || [[ ${locPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locPortFragment='cl,'${locPortId}

		local locGrpMin=(1 7 13 19 25 31)
		local locGrpMax=(6 12 18 24 30 33)
		local locGrp

		for locGrp in {0..5}; do
			if [[ ${locPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

	else
		echo -e "\n  Invalid port type (${locPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

#	echo -e "slot: ${locSlotId_element}"
#	echo -e "port type: ${locPortType}"
#	echo -e "port Id: ${locPortId}"
	
#	echo -e "port fragment: ${locPortFragment}"
	
	if [[ ${locPortCmd:-unspecified} == "demo_show_port" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> This is ${locPortFragment} on slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}"
		else
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}"
		fi

	elif [[ ${locPortCmd:-unspecified} == "demo_create_port" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> creating ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}"
		else
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}"
		fi

	elif [[ ${locPortCmd:-unspecified} == "demo_destroy_port" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> setting ${locPortFragment} to OOS for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}" '[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'
		else
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}" '[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'
		fi

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> destroying ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}"
		else
    		restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}"
		fi
	fi
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_show_port {

	[[ "$1" = "?" ]] && \
		command_port "?" "$FUNCNAME" && \
		return 0

	command_port "-" "$FUNCNAME" "$1" "$2"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_create_port {

	[[ "$1" = "?" ]] && \
		command_port "?" "$FUNCNAME" && \
		return 0

	command_port "-" "$FUNCNAME" "$1" "$2"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_destroy_port {

	[[ "$1" = "?" ]] && \
		command_port "?" "$FUNCNAME" && \
		return 0

	command_port "-" "$FUNCNAME" "$1" "$2"
}


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# O T S i A 	-- assemblies only (OTSi's below)
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# return 0 - no errors
# return 1 - invalid port type
# return 2 - invalid port Id
# return 3 - invalid direction
# return 4 - invalid otsia ID
function command_otsia {

	local locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}$2 [<slotId>] [n1|n2|c1..c33] [tx|rx|bi] [<otsiaId>]${NC}"

	[[ "$1" = "?" ]] && \
		echo -e "${locSyntax}" && \
		return 0

	local locOtsiaCmd=$2
	local locSlotId_element=$3
	local locPort_element=$4
	local locDir_element=$5
	local locOtsiaId_element=$6
	
	[[ ${locSlotId_element:-unspecified} = unspecified ]] && locSlotId_element=${default_demo_slot_cfg}
	[[ ${locPort_element:-unspecified} = unspecified ]] && locPort_element="n1"
	[[ ${locDir_element:-unspecified} = unspecified ]] && locDir_element="bi"
	[[ ${locOtsiaId_element:-unspecified} = unspecified ]] && locOtsiaId_element=1

	local locPortType=${locPort_element//[^a-zA-Z]/}
	local locPortId=${locPort_element//[^0-9]/}

	local locPortGroupFragment
	local locPortFragment

	if [[ ${locPortType:-unspecified} == "n" ]] ; then

		[[ ${locPortId:-unspecified} -ne 1 ]] && \
			[[ ${locPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locPortFragment="nw,${locPortId}"

	elif [[ ${locPortType:-unspecified} == "c" ]] ; then

		if [[ ${locPortId} -lt 1 ]] || [[ ${locPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locPortFragment='cl,'${locPortId}

		local locGrpMin=(1 7 13 19 25 31)
		local locGrpMax=(6 12 18 24 30 33)
		local locGrp

		for locGrp in {0..5}; do
			if [[ ${locPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

	else
		echo -e "\n  Invalid port type (${locPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

	local locOtsiaFragment
	if [[ ${locDir_element:-unspecified} == "rx" ]] ; then
		locOtsiaFragment="otsiarx"
	elif [[ ${locDir_element:-unspecified} == "tx" ]] ; then
		locOtsiaFragment="otsiatx"
	elif [[ ${locDir_element:-unspecified} == "bi" ]] ; then
		locOtsiaFragment="otsia"
	else
		echo -e "\n  Invalid direction (${locDir_element})! Expecting 'rx' or 'tx' or 'bi'" && \
		echo -e "${locSyntax}" && \
		return 3
	fi

	if [[ ${locOtsiaId_element} =~ [^[:digit:]] ]] || \
		[[ ${locOtsiaId_element} -lt 1 ]] || \
		[[ ${locOtsiaId_element} -gt 128 ]] ; then

		echo -e "\n  Invalid OTSiA ID (${locOtsiaId_element})! Expecting 1..128" && \
		echo -e "${locSyntax}" && \
		return 4
	fi

	locOtsiaFragment="${locOtsiaFragment}-${locOtsiaId_element}"

#	echo -e "slot: ${locSlotId_element}"
#	echo -e "port type: ${locPortType}"
#	echo -e "port Id: ${locPortId}"
#	echo -e "dir: ${locDir_element}"
#	echo -e "otsia Id: ${locOtsiaId_element}"
	
#	echo -e "port fragment: ${locPortFragment}"
#	echo -e "otsia fragment: ${locOtsiaFragment}"

	if [[ ${locOtsiaCmd:-unspecified} == "demo_show_otsia" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> This is ${locOtsiaFragment} on ${locPortFragment} on slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}"
		else
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}"
		fi

	elif [[ ${locOtsiaCmd:-unspecified} == "demo_create_otsia" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> creating ${locOtsiaFragment} on ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		local locOosReq='{"sm": {"admin": "oos"}}' 

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosReq}"
		else
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosReq}"
		fi

#		echo -e
#		echo -e "---------------------------------------------------------------------"
#		echo -e "--> (TEMP WORKAROUND) setting ${locOtsiaFragment} on ${locPortFragment} to OOS for slot ${locSlotId_element}"
#		echo -e "---------------------------------------------------------------------"
#
#		local locOosReq='[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'
#
#		if [[ ${locPortType:-unspecified} == "n" ]] ; then
#    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosReq}"
#		else
#    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosReq}"
#		fi

	elif [[ ${locOtsiaCmd:-unspecified} == "demo_destroy_otsia" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> setting ${locOtsiaFragment} on ${locPortFragment} to OOS for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" '[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'
		else
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" '[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'
		fi

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> destroying ${locOtsiaFragment} on ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}"
		else
    		restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}"
		fi
	fi
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_show_otsia {

	[[ "$1" = "?" ]] && \
		command_otsia "?" "$FUNCNAME" && \
		return 0

	command_otsia "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_create_otsia {

	[[ "$1" = "?" ]] && \
		command_otsia "?" "$FUNCNAME" && \
		return 0

	command_otsia "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_destroy_otsia {

	[[ "$1" = "?" ]] && \
		command_otsia "?" "$FUNCNAME" && \
		return 0

	command_otsia "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}



# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# O T S i
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# return 0 - no errors
# return 1 - invalid port type
# return 2 - invalid port Id
# return 3 - invalid direction
# return 4 - invalid otsia ID
# return 4 - invalid otsi ID
function command_otsi {

	local locOtsiCmd=$2
	local locSyntax

	if [[ ${locOtsiCmd:-unspecified} == "demo_show_otsi" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locOtsiCmd} [<slotId>] [n1|n2|c1..c33] [tx|rx|bi] [<otsiaId>] [<otsiId>]${NC}"
	elif [[ ${locOtsiCmd:-unspecified} == "demo_create_otsi" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locOtsiCmd} [<slotId>] [n1|n2|c1..c33] [tx|rx|bi] [<otsiaId>] [<otsiId>] [<slotCtrFreq>] [<slotWidth>]${NC}"
	elif [[ ${locOtsiCmd:-unspecified} == "demo_destroy_otsi" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locOtsiCmd} [<slotId>] [n1|n2|c1..c33] [tx|rx|bi] [<otsiaId>] [<otsiId>]${NC}"
	fi

	[[ "$1" = "?" ]] && \
		echo -e "${locSyntax}" && \
		return 0

	local locSlotId_element=$3
	local locPort_element=$4
	local locDir_element=$5
	local locOtsiaId_element=$6
	local locOtsiId_element=$7
	local locSlotCtrFreq_element=$8
	local locSlotWidth_element=$9
	
	[[ ${locSlotId_element:-unspecified} = unspecified ]] && locSlotId_element=${default_demo_slot_cfg}
	[[ ${locPort_element:-unspecified} = unspecified ]] && locPort_element="n1"
	[[ ${locDir_element:-unspecified} = unspecified ]] && locDir_element="bi"
	[[ ${locOtsiaId_element:-unspecified} = unspecified ]] && locOtsiaId_element=1
	[[ ${locOtsiId_element:-unspecified} = unspecified ]] && locOtsiId_element=1

	if [[ ${locOtsiCmd:-unspecified} == "demo_create_otsi" ]] ; then
		[[ ${locSlotCtrFreq_element:-unspecified} = unspecified ]] && locSlotCtrFreq_element=19130
		[[ ${locSlotWidth_element:-unspecified} = unspecified ]] && locSlotWidth_element=375
	fi

	local locPortType=${locPort_element//[^a-zA-Z]/}
	local locPortId=${locPort_element//[^0-9]/}

	local locPortGroupFragment
	local locPortFragment

	if [[ ${locPortType:-unspecified} == "n" ]] ; then

		[[ ${locPortId:-unspecified} -ne 1 ]] && \
			[[ ${locPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locPortFragment="nw,${locPortId}"

	elif [[ ${locPortType:-unspecified} == "c" ]] ; then

		if [[ ${locPortId} -lt 1 ]] || [[ ${locPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locPortFragment='cl,'${locPortId}

		local locGrpMin=(1 7 13 19 25 31)
		local locGrpMax=(6 12 18 24 30 33)
		local locGrp

		for locGrp in {0..5}; do
			if [[ ${locPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

	else
		echo -e "\n  Invalid port type (${locPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

	local locOtsiaFragment
	if [[ ${locDir_element:-unspecified} == "rx" ]] ; then
		locOtsiaFragment="otsiarx"
	elif [[ ${locDir_element:-unspecified} == "tx" ]] ; then
		locOtsiaFragment="otsiatx"
	elif [[ ${locDir_element:-unspecified} == "bi" ]] ; then
		locOtsiaFragment="otsia"
	else
		echo -e "\n  Invalid direction (${locDir_element})! Expecting 'rx' or 'tx' or 'bi'" && \
		echo -e "${locSyntax}" && \
		return 3
	fi

	if [[ ${locOtsiaId_element} =~ [^[:digit:]] ]] || \
		[[ ${locOtsiaId_element} -lt 1 ]] || \
		[[ ${locOtsiaId_element} -gt 128 ]] ; then

		echo -e "\n  Invalid OTSiA ID (${locOtsiaId_element})! Expecting 1..128" && \
		echo -e "${locSyntax}" && \
		return 4
	fi

	locOtsiaFragment="${locOtsiaFragment}-${locOtsiaId_element}"

	local locOtsiFragment

	if [[ ${locOtsiId_element} =~ [^[:digit:]] ]] || \
		[[ ${locOtsiId_element} -lt 1 ]] || \
		[[ ${locOtsiId_element} -gt 128 ]] ; then

		echo -e "\n  Invalid OTSi ID (${locOtsiId_element})! Expecting 1..128" && \
		echo -e "${locSyntax}" && \
		return 5
	fi

	locOtsiFragment="${locOtsiId_element}"

#	echo -e "slot: ${locSlotId_element}"
#	echo -e "port type: ${locPortType}"
#	echo -e "port Id: ${locPortId}"
#	echo -e "dir: ${locDir_element}"
#	echo -e "otsia Id: ${locOtsiaId_element}"
#	echo -e "otsi Id: ${locOtsiId_element}"
#	echo -e "sltFreq: ${locSlotCtrFreq_element}"
#	echo -e "sltWidth: ${locSlotWidth_element}"
	
#	echo -e "port fragment: ${locPortFragment}"
#	echo -e "otsia fragment: ${locOtsiaFragment}"
#	echo -e "otsi fragment: ${locOtsiFragment}"
	
	if [[ ${locOtsiCmd:-unspecified} == "demo_show_otsi" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> This is ${locOtsiaFragment}/otsia/otsi/${locOtsiFragment} on ${locPortFragment} on slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia/otsi/${locOtsiFragment}"
		else
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia/otsi/${locOtsiFragment}"
		fi

	elif [[ ${locOtsiCmd:-unspecified} == "demo_create_otsi" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> creating ${locOtsiaFragment}/otsia/otsi/${locOtsiFragment} on ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

    	local locJsonArgs='{"sltconf": {"sltfreq": '"${locSlotCtrFreq_element}"', "sltwdth": '"${locSlotWidth_element}"'}}'

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia"
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia/otsi/${locOtsiFragment}" "${locJsonArgs}"
		else
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia"
    		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/otsia/otsi/${locOtsiFragment}" "${locJsonArgs}"
		fi
	fi
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_show_otsi {

	[[ "$1" = "?" ]] && \
		command_otsi "?" "$FUNCNAME" && \
		return 0

	command_otsi "-" "$FUNCNAME" "$1" "$2" "$3" "$4" "$5"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_create_otsi {

	[[ "$1" = "?" ]] && \
		command_otsi "?" "$FUNCNAME" && \
		return 0

	command_otsi "-" "$FUNCNAME" "$1" "$2" "$3" "$4" "$5" "$6" "$7"
}


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# C R S   E x i s t
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# return 0 - no errors
# return 1 - invalid crs ID
# return 2 - invalid from port type
# return 3 - invalid from port Id
# return 4 - invalid from port type
# return 5 - invalid from port Id
# return 6 - invalid otsia ID
function command_crs_exist {

	local locCrsExistCmd=$2
	local locSyntax

	if [[ ${locCrsExistCmd:-unspecified} == "demo_show_crs" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locCrsExistCmd} [<slotId>] [<crsId>]${NC}"
	elif [[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locCrsExistCmd} [<slotId>] [<crsId>] [n1|n2|c1..c33] [n1|n2|c1..c33] [<otsiaId>]${NC}"
	elif [[ ${locCrsExistCmd:-unspecified} == "demo_destroy_crs" ]] ; then
		locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locCrsExistCmd} [<slotId>] [<crsId>]${NC}"
		# locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}${locCrsExistCmd} [<slotId>] [<crsId>] [n1|n2|c1..c33] [n1|n2|c1..c33] [<otsiaId>]${NC}"
	fi

	[[ "$1" = "?" ]] && \
		echo -e "${locSyntax}" && \
		return 0

	local locSlotId_element=$3
	local locCrsId_element=$4
	local locFromPort_element=$5
	local locToPort_element=$6
	local locOtsiaId_element=$7
	
	[[ ${locSlotId_element:-unspecified} = unspecified ]] && locSlotId_element=${default_demo_slot_cfg}
	[[ ${locCrsId_element:-unspecified} = unspecified ]] && locCrsId_element=1

	if [[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] ; then
		[[ ${locFromPort_element:-unspecified} = unspecified ]] && locFromPort_element="c1"
		[[ ${locToPort_element:-unspecified} = unspecified ]] && locToPort_element="n1"
		[[ ${locOtsiaId_element:-unspecified} = unspecified ]] && locOtsiaId_element=1
	fi

	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------

    local locCrsAend='["/me=1/eqh=shelf,1/eqh=slot,'"${locSlotId_element}"'/eq=card/'
    local locCrsZend='["/me=1/eqh=shelf,1/eqh=slot,'"${locSlotId_element}"'/eq=card/'

	local locGrpMin=(1 7 13 19 25 31)
	local locGrpMax=(6 12 18 24 30 33)

	local locFromPortType=${locFromPort_element//[^a-zA-Z]/}
	local locFromPortId=${locFromPort_element//[^0-9]/}
	local locGrp

	local locFromPortGroupFragment
	local locFromPortFragment

	if [[ ${locFromPortType:-unspecified} == "n" ]] ; then

		[[ ${locFromPortId:-unspecified} -ne 1 ]] && \
			[[ ${locFromPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locFromPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locFromPortFragment="nw,${locFromPortId}"
		locCrsAend="${locCrsAend}"'ptp='"${locFromPortFragment}"'/'

	elif [[ ${locFromPortType:-unspecified} == "c" ]] ; then

		if [[ ${locFromPortId} -lt 1 ]] || [[ ${locFromPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locFromPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locFromPortFragment='cl,'${locFromPortId}

		for locGrp in {0..5}; do
			if [[ ${locFromPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locFromPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locFromPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

		locCrsAend="${locCrsAend}"'ptp='"${locFromPortGroupFragment}"'/ptp='"${locFromPortFragment}"'/'

	# else
	elif [[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] ; then
		echo -e "\n  Invalid port type (${locFromPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------

	local locToPortType=${locToPort_element//[^a-zA-Z]/}
	local locToPortId=${locToPort_element//[^0-9]/}

	local locToPortGroupFragment
	local locToPortFragment

	if [[ ${locToPortType:-unspecified} == "n" ]] ; then

		[[ ${locToPortId:-unspecified} -ne 1 ]] && \
			[[ ${locToPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locToPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locToPortFragment="nw,${locToPortId}"
		locCrsZend="${locCrsZend}"'ptp='"${locToPortFragment}"'/'

	elif [[ ${locToPortType:-unspecified} == "c" ]] ; then

		if [[ ${locToPortId} -lt 1 ]] || [[ ${locToPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locToPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locToPortFragment='cl,'${locToPortId}

		for locGrp in {0..5}; do
			if [[ ${locToPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locToPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locToPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

		locCrsZend="${locCrsZend}"'ptp='"${locToPortGroupFragment}"'/ptp='"${locToPortFragment}"'/'

	# else
	elif [[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] ; then
		echo -e "\n  Invalid port type (${locToPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------

	local locOtsiaFragment

	if [[ ${locOtsiaId_element} =~ [^[:digit:]] ]] || \
		[[ ${locOtsiaId_element} -lt 1 ]] || \
		[[ ${locOtsiaId_element} -gt 128 ]] ; then

		[[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] && \
		echo -e "\n  Invalid OTSiA ID (${locOtsiaId_element})! Expecting 1..128" && \
		echo -e "${locSyntax}" && \
		return 4
	fi

	locOtsiaFragment="otsia-${locOtsiaId_element}"

	locCrsAend="${locCrsAend}"'ctp=oms/ctp='"${locOtsiaFragment}"'"],'
	locCrsZend="${locCrsZend}"'ctp=oms/ctp='"${locOtsiaFragment}"'"]'

	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------

	# '{"aendlist":["/me=1/eqh=shelf,1/eqh=slot,6/eq=card/ptp=nw,1/ctp=oms/ctp=otsia-1"],'
	# '"zendlist":["/me=1/eqh=shelf,1/eqh=slot,6/eq=card/ptp=cl,1-6/ptp=cl,1/ctp=oms/ctp=otsia-1"]}'

    local locCrsEnds='{"aendlist":'"${locCrsAend}"'"zendlist":'"${locCrsZend}"'}'

	#local locCrsFragment="crs-${locCrsId_element}"
	local locCrsFragment="${locCrsId_element}"

	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------
	# -----------------------------------------------------------------------------------------

#	echo -e "slot: ${locSlotId_element}"
#	echo -e "crs Id: ${locCrsId_element}"
#	echo -e "from port type: ${locFromPortType}"
#	echo -e "from port Id: ${locFromPortId}"
#	echo -e "to port type: ${locToPortType}"
#	echo -e "to port Id: ${locToPortId}"
#	echo -e "otsia Id: ${locOtsiaId_element}"
	
#	echo -e "from port group fragment: ${locFromPortGroupFragment}"
#	echo -e "from port fragment: ${locFromPortFragment}"
#	echo -e "to port group fragment: ${locToPortGroupFragment}"
#	echo -e "to port fragment: ${locToPortFragment}"
#	echo -e "otsia fragment: ${locOtsiaFragment}"
	
	if [[ ${locCrsExistCmd:-unspecified} == "demo_show_crs" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> This is ${locCrsFragment} for ${locOtsiaFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/crs/${locCrsFragment}"

	elif [[ ${locCrsExistCmd:-unspecified} == "demo_create_crs" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> creating ${locCrsFragment} for ${locOtsiaFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		restCmdBasic "POST" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/crs/${locCrsFragment}" "${locCrsEnds}"

	elif [[ ${locCrsExistCmd:-unspecified} == "demo_destroy_crs" ]] ; then
		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> destroying ${locCrsFragment} for ${locOtsiaFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		restCmdBasic "DELETE" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/crs/${locCrsFragment}"
	fi
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_show_crs {

	[[ "$1" = "?" ]] && \
		command_crs_exist "?" "$FUNCNAME" && \
		return 0

	command_crs_exist "-" "$FUNCNAME" "$1" "$2" 
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_create_crs {

	[[ "$1" = "?" ]] && \
		command_crs_exist "?" "$FUNCNAME" && \
		return 0

	command_crs_exist "-" "$FUNCNAME" "$1" "$2" "$3" "$4" "$5"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_destroy_crs {

	[[ "$1" = "?" ]] && \
		command_crs_exist "?" "$FUNCNAME" && \
		return 0

	command_crs_exist "-" "$FUNCNAME" "$1" "$2" 
}


# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# C R S   A c t i v e
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

# return 0 - no errors
# return 1 - invalid port type
# return 2 - invalid port Id
# return 3 - invalid direction
# return 4 - invalid otsia ID
function command_crs_active {

	local locSyntax="  ${BOLD_WHI}Usage: ${BOLD_RED}$2 [<slotId>] [n1|n2|c1..c33] [tx|rx|bi] [<otsiaId>]${NC}"

	[[ "$1" = "?" ]] && \
		echo -e "${locSyntax}" && \
		return 0

	local locCrsActiveCmd=$2
	local locSlotId_element=$3
	local locPort_element=$4
	local locDir_element=$5
	local locOtsiaId_element=$6
	
	[[ ${locSlotId_element:-unspecified} = unspecified ]] && locSlotId_element=${default_demo_slot_cfg}
	[[ ${locPort_element:-unspecified} = unspecified ]] && locPort_element="n1"
	[[ ${locDir_element:-unspecified} = unspecified ]] && locDir_element="bi"
	[[ ${locOtsiaId_element:-unspecified} = unspecified ]] && locOtsiaId_element=1

	local locPortType=${locPort_element//[^a-zA-Z]/}
	local locPortId=${locPort_element//[^0-9]/}

	local locPortGroupFragment
	local locPortFragment

	if [[ ${locPortType:-unspecified} == "n" ]] ; then

		[[ ${locPortId:-unspecified} -ne 1 ]] && \
			[[ ${locPortId:-unspecified} -ne 2 ]] && \
			echo -e "\n  Invalid Network port ID (${locPortId})! Expecting 1 or 2" && \
			echo -e "${locSyntax}" && \
			return 2

		locPortFragment="nw,${locPortId}"

	elif [[ ${locPortType:-unspecified} == "c" ]] ; then

		if [[ ${locPortId} -lt 1 ]] || [[ ${locPortId} -gt 33 ]] ; then
			echo -e "\n  Invalid Client port ID (${locPortId})! Expecting 1 .. 33"
			echo -e "${locSyntax}"
			return 2
		fi

		locPortFragment='cl,'${locPortId}

		local locGrpMin=(1 7 13 19 25 31)
		local locGrpMax=(6 12 18 24 30 33)
		local locGrp

		for locGrp in {0..5}; do
			if [[ ${locPortId} -ge ${locGrpMin[$locGrp]} ]] && \
				[[ ${locPortId} -le ${locGrpMax[$locGrp]} ]] ; then
				locPortGroupFragment="cl,${locGrpMin[$locGrp]}-${locGrpMax[$locGrp]}"
				break
			fi
		done

	else
		echo -e "\n  Invalid port type (${locPortType})! Expecting 'n' or 'c'"
		echo -e "${locSyntax}"
		return 1
	fi

	local locOtsiaFragment
	if [[ ${locDir_element:-unspecified} == "rx" ]] ; then
		locOtsiaFragment="otsiarx"
	elif [[ ${locDir_element:-unspecified} == "tx" ]] ; then
		locOtsiaFragment="otsiatx"
	elif [[ ${locDir_element:-unspecified} == "bi" ]] ; then
		locOtsiaFragment="otsia"
	else
		echo -e "\n  Invalid direction (${locDir_element})! Expecting 'rx' or 'tx' or 'bi'" && \
		echo -e "${locSyntax}" && \
		return 3
	fi

	if [[ ${locOtsiaId_element} =~ [^[:digit:]] ]] || \
		[[ ${locOtsiaId_element} -lt 1 ]] || \
		[[ ${locOtsiaId_element} -gt 128 ]] ; then

		echo -e "\n  Invalid OTSiA ID (${locOtsiaId_element})! Expecting 1..128" && \
		echo -e "${locSyntax}" && \
		return 4
	fi

	locOtsiaFragment="${locOtsiaFragment}-${locOtsiaId_element}"

#	echo -e "slot: ${locSlotId_element}"
#	echo -e "port type: ${locPortType}"
#	echo -e "port Id: ${locPortId}"
#	echo -e "dir: ${locDir_element}"
#	echo -e "otsia Id: ${locOtsiaId_element}"
	
#	echo -e "port fragment: ${locPortFragment}"
#	echo -e "otsia fragment: ${locOtsiaFragment}"

	local locIsCmd='[{"op": "replace", "path": "/sm/admin", "value": "is"}]'
	local locOosCmd='[{"op": "replace", "path": "/sm/admin", "value": "oos"}]'

	if [[ ${locCrsActiveCmd:-unspecified} == "demo_show_crs_admin" ]] ; then
 
		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> This is ${locOtsiaFragment} on ${locPortFragment} on slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/sm/admin"
		else
    		restCmdBasic "GET" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}/sm/admin"
		fi

	elif [[ ${locCrsActiveCmd:-unspecified} == "demo_enable_crs" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> enabling CRS going TO ${locOtsiaFragment} on ${locPortFragment} for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

#		curl -# -k -X PATCH -H "$hdr2" -H "X-Auth-Token: $token" -d '[{"op": "replace", "path": "/sm/admin", "value": "is"}]' \
#	    	https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${SLOT}/eq/card/ptp/cl,${GROUP}/ptp/cl,${PORT}/ctp/oms/ctp/otsia${AFIX}-${NUMBER}

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locIsCmd}"
		else
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locIsCmd}"
		fi

	elif [[ ${locCrsActiveCmd:-unspecified} == "demo_disable_crs" ]] ; then

		echo -e
		echo -e "---------------------------------------------------------------------"
		echo -e "--> disabling CRS going TO ${locOtsiaFragment} on ${locPortFragment} to OOS for slot ${locSlotId_element}"
		echo -e "---------------------------------------------------------------------"

#		curl -# -k -X PATCH -H "$hdr2" -H "X-Auth-Token: $token" -d '[{"op": "replace", "path": "/sm/admin", "value": "oos"}]' \
#	    	https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${SLOT}/eq/card/ptp/cl,${GROUP}/ptp/cl,${PORT}/ctp/oms/ctp/otsia${AFIX}-${NUMBER}

		if [[ ${locPortType:-unspecified} == "n" ]] ; then
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosCmd}"
		else
    		restCmdBasic "PATCH" "/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_element}/eq/card/ptp/${locPortGroupFragment}/ptp/${locPortFragment}/ctp/oms/ctp/${locOtsiaFragment}" "${locOosCmd}"
		fi
	fi
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_show_crs_admin {

	[[ "$1" = "?" ]] && \
		command_crs_active "?" "$FUNCNAME" && \
		return 0

	command_crs_active "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_enable_crs {

	[[ "$1" = "?" ]] && \
		command_crs_active "?" "$FUNCNAME" && \
		return 0

	command_crs_active "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_disable_crs {

	[[ "$1" = "?" ]] && \
		command_crs_active "?" "$FUNCNAME" && \
		return 0

	command_crs_active "-" "$FUNCNAME" "$1" "$2" "$3" "$4"
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_create_otsia_otsi {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>] [<numOtsiInOtsia>] [<otsiatxId>] [<otsi_1_Id>] [<otsi_2_Id>] [<otsi_3_Id>]${NC}" && \
		return 0

	local locSlotId_createOtsia=$1
	local locNumOtsiInOtsia_createOtsia=$2
	local locOtsiaId_createOtsia=$3
	local locOtsiId_1_createOtsia=$4
	local locOtsiId_2_createOtsia=$5
	local locOtsiId_3_createOtsia=$6

	[[ ${locSlotId_createOtsia:-unspecified} = unspecified ]] && locSlotId_createOtsia=${default_demo_slot_cfg}
	[[ ${locNumOtsiInOtsia_createOtsia:-unspecified} = unspecified ]] && locNumOtsiInOtsia_createOtsia=1
	[[ ${locOtsiaId_createOtsia:-unspecified} = unspecified ]] && locOtsiaId_createOtsia=1
	[[ ${locOtsiId_1_createOtsia:-unspecified} = unspecified ]] && locOtsiId_1_createOtsia=1
	[[ ${locOtsiId_2_createOtsia:-unspecified} = unspecified ]] && locOtsiId_2_createOtsia=2
	[[ ${locOtsiId_3_createOtsia:-unspecified} = unspecified ]] && locOtsiId_3_createOtsia=3

	echo -e
	echo -e "---------------------------------------------------------------------"
	echo -e "--> creating otsiatx-${locOtsiaId_createOtsia} on Network 1 PTP for slot ${locSlotId_createOtsia}"
	echo -e "---------------------------------------------------------------------"
	curl -k -X POST -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
		https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_createOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_createOtsia}

	sleep 1
	echo -e
	echo -e "----------------------------------------------------------------------------------"
	echo -e "--> creating otsiatx-${locOtsiaId_createOtsia}/otsia/otsi-${locOtsiId_1_createOtsia} on Network 1 PTP for slot ${locSlotId_createOtsia}"
	echo -e "----------------------------------------------------------------------------------"
#	curl -k -X POST -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
#		-d '{"sltconf": {"sltfreq": 19245, "sltwdth": 50}}' \
#		https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_createOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_createOtsia}/otsia/otsi/${locOtsiId_1_createOtsia}

    local locSlotFreq=19130
	local locSlotWidth=50
    local locJsonArgs='{"sltconf": {"sltfreq": '"${locSlotFreq}"', "sltwdth": '"${locSlotWidth}"'}}'
	echo -e "locJsonArgs is ${locJsonArgs}"
	curl -k -X POST -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
		-d "${locJsonArgs}" \
		https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_createOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_createOtsia}/otsia/otsi/${locOtsiId_1_createOtsia}

	[[ ${locNumOtsiInOtsia_createOtsia} -ge 2 ]] && \
		sleep 1 && \
		echo -e && \
		echo -e "----------------------------------------------------------------------------------" && \
		echo -e "--> creating otsiatx-${locOtsiaId_createOtsia}/otsia/otsi-${locOtsiId_2_createOtsia} on Network 1 PTP for slot ${locSlotId_createOtsia}" && \
		echo -e "----------------------------------------------------------------------------------" && \
		curl -k -X POST -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
			-d '{"sltconf": {"sltfreq": 19130, "sltwdth": 50}}' \
			https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_createOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_createOtsia}/otsia/otsi/${locOtsiId_2_createOtsia}

	[[ ${locNumOtsiInOtsia_createOtsia} -ge 3 ]] && \
		sleep 1 && \
		echo -e && \
		echo -e "----------------------------------------------------------------------------------" && \
		echo -e "--> creating otsiatx-${locOtsiaId_createOtsia}/otsia/otsi-${locOtsiId_3_createOtsia} on Network 1 PTP for slot ${locSlotId_createOtsia}" && \
		echo -e "----------------------------------------------------------------------------------" && \
		curl -k -X POST -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
			-d '{"sltconf": {"sltfreq": 19200, "sltwdth": 50}}' \
			https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_createOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_createOtsia}/otsia/otsi/${locOtsiId_3_createOtsia}

	echo -e
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_remove_otsia {

	[[ "$1" = "?" ]] && \
		echo -e "  ${BOLD_WHI}Usage: ${BOLD_RED}$FUNCNAME [<slotId>] [<otsiatxId>]${NC}" && \
		return 0

	local locSlotId_removeOtsia=$1
	local locOtsiaId_removeOtsia=$2

	[[ ${locSlotId_removeOtsia:-unspecified} = unspecified ]] && locSlotId_removeOtsia=${default_demo_slot_cfg}
	[[ ${locOtsiaId_removeOtsia:-unspecified} = unspecified ]] && locOtsiaId_removeOtsia=1

	echo -e
	echo -e "---------------------------------------------------------------------"
	echo -e "--> setting otsiatx-${locOtsiaId_removeOtsia} to OOS on Network 1 PTP for slot ${locSlotId_removeOtsia}"
	echo -e "---------------------------------------------------------------------"
	curl -k -X PATCH -H "Content-Type:application/json-patch+json; ext=nn" -H "X-Auth-Token:${token}" -d '[{"op": "replace", "path": "/admin", "value": "oos"}]' \
		https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_removeOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_removeOtsia}/sm

	echo -e
	echo -e "--------------------------------------------------------------------"
	echo -e "--> deleting otsiatx-${locOtsiaId_removeOtsia} on Network 1 PTP for slot ${locSlotId_removeOtsia}"
	echo -e "--------------------------------------------------------------------"
	curl -k -X DELETE -H "Content-Type:application/json; ext=nn" -H "X-Auth-Token:${token}" \
		https://$target/mit/me/1/eqh/shelf,1/eqh/slot,${locSlotId_removeOtsia}/eq/card/ptp/nw,1/ctp/oms/ctp/otsiatx-${locOtsiaId_removeOtsia}

	echo -e
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_funcs {

	echo -e
	echo -e "-------------------------"
	echo -e "Available Demo Functions:"
	echo -e "-------------------------"
	echo -e

	declare -F | grep demo | grep -v demo_func | grep -v rest_hookup | awk '{ print $3 }'
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

function demo_ecm_ipv4_rest_hookup {

	local locDemoEcmIPV4=$1

	echo -e "---------------------------"
	echo -e "ECM IPV4 REST Hookup Status"
	echo -e "---------------------------"

	# demo ECM IPV4 specified
	if [[ ${locDemoEcmIPV4:-unspecified} != unspecified ]] ; then
		if [[ ${target:-unspecified} != unspecified ]] ; then
			restLogout ${target}
		fi
		sleep 2
		restLogin ${locDemoEcmIPV4}
		[[ $? -ne 0 ]] && return 1

	# demo ECM IPV4 not specified
	else
		if [[ ${target:-unspecified} = unspecified ]] ; then
			echo -e "\n ${BOLD_WHI}--> ${BOLD_RED}Need to attach to ECM IPV4 for REST interface for demo!${NC}"
			return 2
		fi
	fi

	restWho
}

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------

if ! [[ -z ${1} ]] || [[ ${target:-unspecified} != unspecified ]] ; then

	demo_funcs

	echo -e

	demo_ecm_ipv4_rest_hookup $1

else
	# this only works if script is not sourced
	# echo -e " ${BOLD_WHI}Syntax: ${BOLD_RED}$(basename "$0") <ECM IPV4>${NC}"
	echo -e " ${BOLD_WHI}Syntax: ${BOLD_RED}$BASH_SOURCE <ECM IPV4>${NC}"
fi

# ----------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------


