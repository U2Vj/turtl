<template>
  <div>
    <b-button v-b-toggle.sidebar-variant>Show Sidebar</b-button>
    <b-sidebar id="sidebar-variant" title="Turtl" bg-variant="dark" text-variant="light" shadow width="190px">
      <div class="px-3 py-2">
        <div>
          <b-button-group vertical>
            <b-button>Overview</b-button>
            <b-button>Tasks</b-button>
            <b-button>Issues</b-button>
            <b-button>Container</b-button>
            <b-button>Help</b-button>
          </b-button-group>
          <div class="sidebar-logo">
            <TitleLogo/>
          </div>
        </div>
      </div>
    </b-sidebar>
  </div>
</template>

<script>
// @ is an alias to /src
import TitleLogo from '@/components/TitleLogo.vue'

export default {
    name: 'Home',
    components: {
        TitleLogo
    }
}
</script>

<style scoped>
.sidebar-logo{
  width: 400%;
  height: 400%;
}
</style>
