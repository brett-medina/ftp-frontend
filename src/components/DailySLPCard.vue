<template>
<generic-card :showGraph="true"
              :data="getGraphData"
              :header="header"
              :bottomText="recentIncreaseText"
              :icon="icon"
              :midText="todaysIncrease"
/>
</template>

<script>
import { mapGetters } from "vuex"
import GenericCard from './GenericCard.vue'

export default {
    name: "daily-slp-card",
    props:{
        header: String,
        icon: String,
        data: Array
    },
    components:{
        GenericCard
    },
    data(){
      return{
      }
    },
    computed:{
        ...mapGetters(['getCurrentUser', 'getToken']),
        getGraphData(){
            let chartData = []
            let tempData = {}
            this.data.forEach(function(scholar){
                for (let i = scholar.length-1; i > 0; i--){
                    let diff = 0
                    const prevBal = scholar[i-1].slp_bal
                    const currBal = scholar[i].slp_bal
                    diff = currBal - prevBal
                    const date = Date.parse(scholar[i].created_at)
                    const diffAdd = tempData[date] ? tempData[date] + diff : diff
                    tempData[date] = diffAdd
                }
            })
            Object.entries(tempData).sort().forEach(([key, value])=>{
                chartData.push([new Date(+key), value])
            })
            return chartData
        },
        getRecentIncrease(){
            const graphData = this.getGraphData 
            if (graphData.length > 0) {
                if (graphData.length == 1){
                    return graphData[0][1]
                }else{
                    return graphData[graphData.length-1][1] - graphData[graphData.length-2][1]
                }
            }
        },
        todaysIncrease(){
            const graphData = this.getGraphData 
            if (graphData.length > 0) {
                let returnString = graphData[graphData.length-1][1] 
                return returnString >= 0 ? '+' + returnString : returnString;
            }
            return 0
        },
        recentIncreaseText(){
            let returnString = this.getRecentIncrease + ' compared to yesterday'
            return this.getRecentIncrease >= 0 ? '+' + returnString : returnString;
        },
    },
    methods:{
    },
    created(){
    }
}
</script>

<style scoped>
.photo-card{
    margin-left:auto;
    margin-right:auto;
    margin-top: 20px;
}
.user-link{
  color: black;
}
.inner-card .card-body{
  padding:0;
}
</style>