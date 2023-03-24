<script setup lang="ts">
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'
import { ref } from 'vue'
import { onMounted } from 'vue'

const term = ref<Terminal>()
const socket = ref<WebSocket>()

onMounted(() => {
  term.value = new Terminal({
    cursorBlink: true,
    cols: 60,
    rows: 20
  })

  socket.value = new WebSocket(import.meta.env.VITE_WS_URL)
  const attachAddon = new AttachAddon(socket.value)
  term.value.loadAddon(attachAddon)

  const fitAddon = new FitAddon()
  term.value.loadAddon(fitAddon)
  //term.value._initialized = true

  const terminalContainer = document.getElementById('terminal-container')
  if (terminalContainer) {
    term.value.open(terminalContainer)
  }

  fitAddon.fit()
})

/* beforeDestroy () {
    this.terminalSocket.close()
// this.term.destroy()
} */
</script>

<template>
  <div>
    <div :id="'terminal-container'"></div>
  </div>
</template>

<!-- <style scoped>
.console {
  width: auto;
  overflow: scroll;
}
</style> -->

<style src="xterm/css/xterm.css"></style>
