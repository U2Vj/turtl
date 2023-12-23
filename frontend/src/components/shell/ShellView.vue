<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

const term = ref<Terminal>();
const socket = ref<WebSocket>();

onMounted(() => {
  term.value = new Terminal({
    cursorBlink: true,
    convertEol: true,
  });

  socket.value = new WebSocket(import.meta.env.VITE_WS_URL);

  const fitAddon = new FitAddon();
  term.value.loadAddon(fitAddon);

  const terminalContainer = document.getElementById('terminal-container');
  if (terminalContainer) {
    term.value.open(terminalContainer);
  }

  fitAddon.fit();

  let commandBuffer = '';

  term.value.onKey(({ key, domEvent }) => {
    if (domEvent.key === 'Enter') {
      // Only send the command when Enter is pressed
      socket.value?.send(JSON.stringify({ message: commandBuffer }));
      commandBuffer = '';
    } else if (domEvent.key === 'Backspace') {
      // Handle backspace
      if (commandBuffer.length > 0) {
        commandBuffer = commandBuffer.slice(0, -1);
        term.value?.write('\b \b');
      }
    } else {
      // Accumulate other keys into commandBuffer
      commandBuffer += key;
      term.value?.write(key);
    }
  });

  // Handle incoming messages from the WebSocket
  socket.value.onmessage = (event) => {
    term.value?.write(event.data);
  };
});
</script>

<template>
  <div>
    <div :id="'terminal-container'"></div>
  </div>
</template>

<style src="xterm/css/xterm.css"></style>