<template>
    <b-container fluid>
        <b-row>
            <b-col cols="12" lg="1" class="p-0"><Navbar/></b-col>
            <b-col cols="12" lg="11" class="p-0 p-lg-2">
                <b-card :title="classroom.room">
                    <Shell />
                </b-card>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
import Navbar from '@/components/Navbar.vue'
import Shell from '@/components/Shell.vue'
import { mapState } from 'vuex'

export default {
    components: {
        Navbar,
        Shell
    },
    computed: {
        ...mapState('classroom', {
            classroom: state => state.current
        })
    }
}
</script>

<style scoped>
</style>
