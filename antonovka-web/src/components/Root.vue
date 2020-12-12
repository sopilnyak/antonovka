<template>
  <div>
    <div id="results">
      <div class="button-wrapper">
        <div class="button"><font-awesome-icon icon="plus" /></div>
        <input type="file" id="file" ref="file" v-on:change="upload()" />
      </div>
      <div
        v-for="task in tasks.slice().reverse()"
        class="image"
        v-tooltip="{ content: tooltip(task.result) }"
        :key="task.taskId"
        :style="{
          backgroundImage: 'url(' + task.imageUrl + ')',
          borderColor: borderColor(task.result),
          opacity: imageOpacity(task.result),
        }"
      >
        <div class="spinner-wrapper">
          <div
            class="spinner"
            :style="{
              visibility: task.result == null ? 'visible' : 'hidden',
            }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const url = "http://localhost:5000/api";

class Task {
  constructor(taskId, imageUrl) {
    this.taskId = taskId;
    this.imageUrl = imageUrl;
    this.result = null;
  }
}

export default {
  data() {
    return {
      tasks: [],
    };
  },
  methods: {
    upload: function() {
      this.file = this.$refs.file.files[0];
      let formData = new FormData();
      formData.append("file", this.file);
      this.$refs.file.value = null;
      axios
        .post(`${url}/predict`, formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          let imageUrl = `${url}/image/${response.data.filename}`;
          this.tasks.push(new Task(response.data.task_id, imageUrl));
          setTimeout(
            (taskId) => this.getTaskResult(taskId),
            1000,
            response.data.task_id
          );
        });
    },

    getTaskResult: function(taskId) {
      axios.get(`${url}/${taskId}/status`).then((response) => {
        if (response.data.result != "") {
          let task = this.tasks.find((value) => value.taskId == taskId);
          task.result = response.data.result;
        } else {
          setTimeout((taskId) => this.getTaskResult(taskId), 1000, taskId);
        }
      });
    },

    borderColor: function(taskResult) {
      if (taskResult == null) {
        return "gray";
      }
      if (taskResult == "true") {
        return "#EA2027";
      }
      return "#00c853";
    },

    imageOpacity: function(taskResult) {
      return taskResult == null ? 0.5 : 1;
    },

    tooltip: function(taskResult) {
      if (taskResult == "false") {
        return "Яблоня здорова!";
      }
      if (taskResult == "true") {
        return "Яблоня больна :(";
      }
    },
  },
};
</script>

<style>
#results {
  font-size: 2em;
  width: 70%;
  min-width: 20em;
  margin: 2em auto;
}

.image {
  display: inline-block;
  width: 6em;
  height: 6em;
  margin: 0.5em;
  border: 5px solid;
  background-position: center center;
  background-size: cover;
  box-shadow: 0px 0px 33px -7px #5e5e5e;
}

.button-wrapper {
  display: inline-block;
  width: 6em;
  height: 6em;
  margin: 0.5em;
  border: 5px rgba(150, 155, 163, 0.4) dashed;
  background-position: center center;
  background-size: cover;
  position: relative;
  overflow: hidden;
  box-shadow: 0px 0px 33px -7px #5e5e5e;
}

.button {
  background-color: #eff0f4;
  padding: 25px 20px;
  border: 0;
  font-size: 3em;
  color: rgba(150, 155, 163, 0.7);
}

.button-wrapper input[type="file"] {
  height: 6em;
  font-size: 100px;
  position: absolute;
  left: 0;
  top: 0;
  opacity: 0;
}

.spinner-wrapper {
  width: 6em;
  height: 6em;
}

.spinner {
  margin: 30% auto;
  height: 60px;
  width: 60px;
  -webkit-animation: rotation 0.6s infinite linear;
  -moz-animation: rotation 0.6s infinite linear;
  -o-animation: rotation 0.6s infinite linear;
  animation: rotation 0.6s infinite linear;
  border-left: 6px solid rgba(0, 174, 239, 0.15);
  border-right: 6px solid rgba(0, 174, 239, 0.15);
  border-bottom: 6px solid rgba(0, 174, 239, 0.15);
  border-top: 6px solid rgba(0, 174, 239, 1);
  border-radius: 100%;
}

@-webkit-keyframes rotation {
  from {
    -webkit-transform: rotate(0deg);
  }
  to {
    -webkit-transform: rotate(359deg);
  }
}
@-moz-keyframes rotation {
  from {
    -moz-transform: rotate(0deg);
  }
  to {
    -moz-transform: rotate(359deg);
  }
}
@-o-keyframes rotation {
  from {
    -o-transform: rotate(0deg);
  }
  to {
    -o-transform: rotate(359deg);
  }
}
@keyframes rotation {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(359deg);
  }
}

.tooltip {
  display: block !important;
  z-index: 10000;
}

.tooltip .tooltip-inner {
  background: #576574;
  color: white;
  border-radius: 10px;
  padding: 5px 10px 7px;
}

.tooltip .tooltip-arrow {
  width: 0;
  height: 0;
  border-style: solid;
  position: absolute;
  margin: 5px;
  border-color: #576574;
  z-index: 1;
}

.tooltip[x-placement^="top"] {
  margin-bottom: 5px;
}

.tooltip[x-placement^="top"] .tooltip-arrow {
  border-width: 5px 5px 0 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  bottom: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="bottom"] {
  margin-top: 5px;
}

.tooltip[x-placement^="bottom"] .tooltip-arrow {
  border-width: 0 5px 5px 5px;
  border-left-color: transparent !important;
  border-right-color: transparent !important;
  border-top-color: transparent !important;
  top: -5px;
  left: calc(50% - 5px);
  margin-top: 0;
  margin-bottom: 0;
}

.tooltip[x-placement^="right"] {
  margin-left: 5px;
}

.tooltip[x-placement^="right"] .tooltip-arrow {
  border-width: 5px 5px 5px 0;
  border-left-color: transparent !important;
  border-top-color: transparent !important;
  border-bottom-color: transparent !important;
  left: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip[x-placement^="left"] {
  margin-right: 5px;
}

.tooltip[x-placement^="left"] .tooltip-arrow {
  border-width: 5px 0 5px 5px;
  border-top-color: transparent !important;
  border-right-color: transparent !important;
  border-bottom-color: transparent !important;
  right: -5px;
  top: calc(50% - 5px);
  margin-left: 0;
  margin-right: 0;
}

.tooltip.popover .popover-inner {
  background: #f9f9f9;
  color: black;
  padding: 24px;
  border-radius: 5px;
  box-shadow: 0 5px 30px rgba(black, 0.1);
}

.tooltip.popover .popover-arrow {
  border-color: #f9f9f9;
}

.tooltip[aria-hidden="true"] {
  visibility: hidden;
  opacity: 0;
  transition: opacity 0.15s, visibility 0.15s;
}

.tooltip[aria-hidden="false"] {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.15s;
}
</style>
