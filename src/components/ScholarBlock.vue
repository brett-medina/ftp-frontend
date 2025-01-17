<template>
    <b-row class="ml-1 mb-4 ">
        
        <b-modal v-if="showGraph" title="Daily SLP Graph"
            :id="'SLPDaily'+scholar.scholar_id"
            size="md"
            hide-footer
            hide-header>
            <line-chart  :data="getDailyGraphData">
            </line-chart>
        </b-modal>
        
        <b-modal v-if="showGraph" title="Weekly SLP Graph"
            :id="'SLPWeekly'+scholar.scholar_id"
            size="md"
            hide-footer
            hide-header>
            <line-chart  :data="getWeeklyGraphData">
            </line-chart>
        </b-modal>

        <b-col cols="0"> 
            <b-form-checkbox
                :id="this.scholar.id"
            />
        </b-col>
        <b-col cols="2">
            {{scholar.name}}
        </b-col>
        <b-col cols="2">
            {{truncatedAddress}}
        <b-icon-clipboard v-b-tooltip.hover :title="getHoverTip" @click="copyRonin" @mouseleave="copied=false">
        </b-icon-clipboard>
        </b-col>
        <b-col cols="2">
            {{truncatedPersonalAddress}}
            <b-icon-clipboard v-b-tooltip.hover :title="getHoverTip" @click="copyPersonalRonin" @mouseleave="copied=false">
            </b-icon-clipboard>
        </b-col>
        <b-col cols="1">
            NULL
        </b-col>
        <b-col cols="2">
            <b-icon-eye v-b-modal="'SLPDaily'+scholar.scholar_id" />
            {{dailySlp}}
            
        </b-col>
        <b-col cols="2">
            <b-icon-eye v-b-modal="'SLPWeekly'+scholar.scholar_id" />
            {{weeklySlp}}
        </b-col>
    </b-row>
</template>

<script>
import { mapGetters } from 'vuex'

export default {
    name: "scholar-block",
    components: {
        
    },
    props:{
        scholarSnapshotData: Array
    },
    data(){
        return{
            copied: false
        }
    },
    computed:{
        ...mapGetters(['getCurrentUser']),
        dailySlp(){
            let prev_bal = null
            //reduces the weekly snapshot into last 7 days and gets average of the slp gains between them
            return parseInt(Object.entries(this.scholarSnapshotData.slice(1).slice(-7)).reduce(function (total, pair) {
                    const [_, value] = pair;
                    let diff = 0
                    if (prev_bal){
                        diff = value.slp_bal - prev_bal
                    }
                    prev_bal = value.slp_bal
                    return total + diff;
                    }, 0) / 7)
        },
        showGraph(){
            return true
        },
        weeklySlp(){
            //reduces the last 7 days for the gains 
            let prev_bal = null
            return parseInt(Object.entries(this.scholarSnapshotData.slice(1).slice(-7)).reduce(function (total, pair) {
                    const [_, value] = pair;
                    let diff = 0
                    if (prev_bal){
                        diff = value.slp_bal - prev_bal
                    }
                    prev_bal = value.slp_bal
                    return total + diff;
                    }, 0))
        },
        getDailyGraphData(){
            let chartData = []
            let tempData = {}
            for (let i = this.scholarSnapshotData.length-1; i > 0; i--){
                let diff = 0
                const prevBal = this.scholarSnapshotData[i-1].slp_bal
                const currBal = this.scholarSnapshotData[i].slp_bal
                diff = currBal - prevBal
                const date = Date.parse(this.scholarSnapshotData[i].created_at)
                const timestamp = date//yr + "-" + mo + "-" + day
                const diffAdd = tempData[timestamp] ? tempData[timestamp] + diff : diff
                tempData[timestamp] = diffAdd
            }
            Object.entries(tempData).sort().forEach(([key, value])=>{
                chartData.push([new Date(+key), value])
            })
            return chartData
        },
        getWeeklyGraphData(){
            let chartData = []
            let tempData = {}
            let day = 0
            let weeklySlpTotal = 1
            //iterate until > 0 because we don't want from day 0, we want the delta from 0->1
            for (let i = this.scholarSnapshotData.length-1; i > 0; i--){
                let diff = 0
                const prevBal = this.scholarSnapshotData[i-1].slp_bal
                const currBal = this.scholarSnapshotData[i].slp_bal
                diff = currBal - prevBal
                if (day < 6){
                    day++
                    weeklySlpTotal += diff
                }else{
                    const date = Date.parse(this.scholarSnapshotData[i].created_at)
                    const diffAdd = tempData[date] ? tempData[date] + weeklySlpTotal : weeklySlpTotal
                    tempData[date] = diffAdd
                    day = 0
                    weeklySlpTotal = 0
                }
            }
            Object.entries(tempData).sort().forEach(([key, value])=>{
                chartData.push([new Date(+key), value])
            })
            return chartData
        },
        scholar(){
            return this.scholarSnapshotData[0]
        },
        truncatedAddress(){
            return "..."+this.scholar.address.slice(-8)
        },
        truncatedPersonalAddress(){
            return "..."+this.scholar.personal_address.slice(-8)
        },
        getHoverTip(){
            return this.copied ? "Copied!" : "Copy to Clipboard"
        },
    },
    methods:{
        copyPersonalRonin(){
            console.log(this.scholar.personal_address)
            this.copied = true
        },
        copyRonin(){
            console.log(this.scholar.address)
            this.copied = true
        }
    }
}
</script>

<style>
.info-row{
    height: 33%;
}
.info-text{
    margin-top:auto;
}
.btn:focus,.btn:active {
   outline: none !important;
   box-shadow: none;
}

</style>