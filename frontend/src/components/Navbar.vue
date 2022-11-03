<template>
    <div class="sidebar p-1 mb-2">
        <div>
            <b-button-group vertical size=md class="w-100">
                <b-button class="p-1"
                          v-for="item in items" :key="item.topic"
                          @click="handleChangeContent(item.name)"
                >
                    {{item.topic}}
                </b-button>
            </b-button-group>
        </div>
    </div>
</template>

<script>
export default {
    data () {
        return {
            fields: ['topic', 'name'],
            items: [
                { topic: 'Overview', name: 'overview' },
                { topic: 'Tasks', name: 'tasks' },
                { topic: 'Issues', name: 'issues' },
                { topic: 'Container', name: 'container' },
                { topic: 'Help', name: 'help' }
            ]
        }
    },
    methods: {
        async handleChangeContent (name) {
            this.$router.push({ name: name }) // Link to routes does not work properly
        }
    }
}
</script>

<style scoped>
.sidebar{
    background-color:#8ddce8; /* Light Blue */
}
</style>
