<template>
  <div>
    <div class="console" :id="'terminal-docker'"></div>
  </div>
</template>

<script>
import { Terminal } from 'xterm'
import { FitAddon } from 'xterm-addon-fit'
import { AttachAddon } from 'xterm-addon-attach'
export default {
    name: 'Shell',
    props: {
        terminal: {
            type: Object,
            default: () => {}
        }
    },
    data () {
        return {
            term: null,
            terminalSocket: null
        }
    },
    methods: {
    },
    mounted () {
        const terminalContainer = document.getElementById('terminal-docker')
        this.term = new Terminal({
            cursorBlink: true,
            cols: 60,
            rows: 20
        })
        this.term.open(terminalContainer)
        this.terminalSocket = new WebSocket('ws://127.0.0.1:8000/shell')
        const attachAddon = new AttachAddon(this.terminalSocket)
        const fitAddon = new FitAddon()
        this.term.loadAddon(fitAddon)
        this.term.loadAddon(attachAddon)
        this.term._initialized = true
        fitAddon.fit()
    },
    beforeDestroy () {
        this.terminalSocket.close()
    // this.term.destroy()
    }
}
</script>

<style scoped>
.console{
    width: auto;
    overflow: scroll;
}
</style>
