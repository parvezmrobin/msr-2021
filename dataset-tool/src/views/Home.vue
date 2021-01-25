<template>
  <div class="container-fluid">
    <form class="row" @submit.prevent="filterEntries">
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixCommitSHA1"
          placeholder="Fix Commit SHA1"
          title="Fix Commit SHA1"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixCommitParentSHA1"
          placeholder="Fix Commit Parent SHA1"
          title="Fix Commit Parent SHA1"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="bugFilePath"
          placeholder="Bug File Path"
          title="Bug File Path"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixPatch"
          placeholder="Fix Patch"
          title="Fix Patch"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="projectName"
          placeholder="Project Name"
          title="Project Name"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugLineNum"
          placeholder="Bug Line Number"
          title="Bug Line Number"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugNodeStartChar"
          placeholder="Bug Node Start Char"
          title="Bug Node Start Char"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugNodeLength"
          placeholder="Bug Node Length"
          title="Bug Node Length"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixLineNum"
          placeholder="Fix Line Number"
          title="Fix Line Number"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixNodeStartChar"
          placeholder="Fix Node Start Char"
          title="Fix Node Start Char"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixNodeLength"
          placeholder="Fix Node Length"
          title="Fix Node Length"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="sourceBeforeFix"
          placeholder="Source Before Fix"
          title="Source Before Fix"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="sourceAfterFix"
          placeholder="Source After Fix"
          title="Source After Fix"
        />
      </div>
      <div class="col-3 d-flex align-items-center">
        <div class="form-check form-check-inline">
          <input
            class="form-check-input"
            type="checkbox"
            v-model="group"
            id="group"
          />
          <label class="form-check-label" for="group">
            Group By Commit + File
          </label>
        </div>
      </div>
      <div class="col-3">
        <button class="btn btn-info" type="submit">
          <span
            v-show="isLoading"
            class="spinner-border spinner-border-sm"
            role="status"
          >
            <span class="sr-only">Loading...</span>
          </span>
          Search
        </button>
      </div>
    </form>
    <div class="row">
      <div class="col-12">
        <table class="table mt-3">
          <thead>
            <tr>
              <th />
              <th>Fix Commit SHA1</th>
              <th v-show="false">Fix Commit Parent SHA1</th>
              <th>Bug File Path</th>
              <th>Fix Patch</th>
              <th>Project Name</th>
              <th>Source Before Fix</th>
              <th>Source After Fix</th>
              <th>Bug Line Num</th>
              <th>Bug Node Start Char</th>
              <th>Bug Node Length</th>
              <th>Fix Line Num</th>
              <th>Fix Node Start Char</th>
              <th>Fix Node Length</th>
            </tr>
          </thead>
          <tbody>
            <tr :key="i" v-for="(entry, i) in filteredEntries">
              <td>
                <button
                  class="btn"
                  :class="expanded[i] ? 'btn-warning' : 'btn-info'"
                  @click="toggleExpansion(i)"
                >
                  {{ expanded[i] ? "-" : "+" }}
                </button>
              </td>
              <td>{{ entry.fixCommitSHA1 }}</td>
              <td v-show="false">{{ entry.fixCommitParentSHA1 }}</td>
              <td
                v-show="!expanded[i]"
                class="text-left"
              >
                {{ entry.bugFilePath }}
              </td>
              <td class="text-left" :colspan="expanded[i] ? 2 : 1">
                <Diff2Html v-if="expanded[i]" :value="entry.fixPatch" />
                <code v-else>{{ entry.fixPatch.slice(0, 30) }}</code>
              </td>
              <td>{{ entry.projectName }}</td>
              <td class="text-left" :title="entry.sourceBeforeFix">
                <code>
                  {{ entry.sourceBeforeFix.slice(0, 10) }} ...
                  {{ entry.sourceBeforeFix.slice(-10) }}
                </code>
              </td>
              <td class="text-left" :title="entry.sourceAfterFix">
                <code>
                  {{ entry.sourceAfterFix.slice(0, 10) }} ...
                  {{ entry.sourceAfterFix.slice(-10) }}
                </code>
              </td>
              <td>{{ entry.bugLineNum }}</td>
              <td>{{ entry.bugNodeStartChar }}</td>
              <td>{{ entry.bugNodeLength }}</td>
              <td>{{ entry.fixLineNum }}</td>
              <td>{{ entry.fixNodeStartChar }}</td>
              <td>{{ entry.fixNodeLength }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import axios from "axios";
import Diff2Html from "@/components/Diff2Html.vue";

interface SStuBs {
  bugType: string;
  fixCommitSHA1: string;
  fixCommitParentSHA1: string;
  bugFilePath: string;
  fixPatch: string;
  projectName: string;
  bugLineNum: number;
  bugNodeStartChar: number;
  bugNodeLength: number;
  fixLineNum: number;
  fixNodeStartChar: number;
  fixNodeLength: number;
  sourceBeforeFix: string;
  sourceAfterFix: string;
  group: boolean;
}

export default Vue.extend({
  components: { Diff2Html },
  data() {
    return {
      fixCommitSHA1: "",
      fixCommitParentSHA1: "",
      bugFilePath: "",
      fixPatch: "",
      projectName: "",
      bugLineNum: "" as string | number,
      bugNodeStartChar: "" as string | number,
      bugNodeLength: "" as string | number,
      fixLineNum: "" as string | number,
      fixNodeStartChar: "" as string | number,
      fixNodeLength: "" as string | number,
      sourceBeforeFix: "",
      sourceAfterFix: "",
      filteredEntries: [] as SStuBs[],
      expanded: [] as boolean[],
      isLoading: false,
      group: false
    };
  },
  watch: {
    group() {
      this.filterEntries();
    },
  },
  methods: {
    toggleExpansion(index: number) {
      this.expanded.splice(index, 1, !this.expanded[index]);
    },
    filterEntries: async function() {
      this.isLoading = true;
      const bugsLarge = await axios.get<SStuBs[]>("/bugsLarge.json");
      const entries = bugsLarge.data;
      let filteredEntries = entries.filter(entry => {
        return (
          entry.fixCommitSHA1.includes(this.fixCommitSHA1) &&
          entry.fixCommitParentSHA1.includes(this.fixCommitParentSHA1) &&
          entry.bugFilePath.includes(this.bugFilePath) &&
          entry.fixPatch.includes(this.fixPatch) &&
          entry.projectName.includes(this.projectName) &&
          (this.bugLineNum ? entry.bugLineNum === this.bugLineNum : true) &&
          (this.bugNodeStartChar
            ? entry.bugNodeStartChar === this.bugNodeStartChar
            : true) &&
          (this.bugNodeLength
            ? entry.bugNodeLength === this.bugNodeLength
            : true) &&
          (this.fixLineNum ? entry.fixLineNum === this.fixLineNum : true) &&
          (this.fixNodeStartChar
            ? entry.fixNodeStartChar === this.fixNodeStartChar
            : true) &&
          (this.fixNodeLength
            ? entry.fixNodeLength === this.fixNodeLength
            : true) &&
          entry.sourceBeforeFix.includes(this.sourceBeforeFix) &&
          entry.sourceAfterFix.includes(this.sourceAfterFix)
        );
      });

      const filterCache: string[] = [];
      if (this.group) {
        filteredEntries = filteredEntries.filter(entry => {
          if (filterCache.includes(entry.fixCommitSHA1 + entry.bugFilePath)) {
            return false;
          }
          filterCache.push(entry.fixCommitSHA1 + entry.bugFilePath);
          return true;
        });
      }
      this.filteredEntries = filteredEntries.slice(0, 50);
      if (this.filteredEntries.length === 1) {
        this.expanded = [true];
      } else {
        this.expanded = filteredEntries.map(() => false);
      }

      this.isLoading = false;
    }
  }
});
</script>

<style scoped lang="scss">
@import "../assets/bootstrap@4.5.3.css";
</style>
