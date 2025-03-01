<template>
	<div id="result">{{ result }}</div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const result = ref<any>()
const xhr = new XMLHttpRequest();
const searchParams = new URLSearchParams(window.location.search);
const type = searchParams.get("type") || "";
const msg = searchParams.get("msg") || "";

const chat = () => {
  xhr.open("POST", "https://tools.mgtv100.com/external/v1/pear/deepseek", false); // 第三个参数设置为 false 表示同步请求
  xhr.setRequestHeader("Content-Type", "application/json");

  try {
    xhr.send(JSON.stringify({ content: msg.trim() }));
    if (xhr.status === 200) result.value = JSON.parse(xhr.responseText);
    else result.value = JSON.parse(String({"status": "error", "code": 500, "data": {"message": "请求失败"}}));
  } catch (err) {
    result.value = JSON.parse(String({"status": "error", "code": 500, "data": {"message": err}}));
  }
};

if (type.trim() != '' && msg.trim() != '') {
	if (type.trim() == 'chat') chat();
}
</script>

<style scoped lang="less"></style>