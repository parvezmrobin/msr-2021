<template>
  <div class="container-fluid">
    <form class="row" @submit.prevent="filterEntries">
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixCommitSHA1"
          placeholder="Fix Commit SHA1"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixCommitParentSHA1"
          placeholder="Fix Commit Parent SHA1"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="bugFilePath"
          placeholder="Bug File Path"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="fixPatch"
          placeholder="Fix Patch"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="projectName"
          placeholder="Project Name"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugLineNum"
          placeholder="Bug Line Number"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugNodeStartChar"
          placeholder="Bug Node Start Char"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="bugNodeLength"
          placeholder="Bug Node Length"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixLineNum"
          placeholder="Fix Line Number"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixNodeStartChar"
          placeholder="Fix Node Start Char"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model.number="fixNodeLength"
          placeholder="Fix Node Length"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="sourceBeforeFix"
          placeholder="Source Before Fix"
        />
      </div>
      <div class="col-3">
        <input
          type="text"
          class="form-control"
          v-model="sourceAfterFix"
          placeholder="Source After Fix"
        />
      </div>
      <div class="col-9">
        <button class="btn btn-info" type="submit">Search</button>
      </div>
    </form>
    <div class="row">
      <div class="col-12">
        <table class="table mt-3">
          <thead>
            <tr>
              <th>Fix Commit SHA1</th>
              <th>Fix Commit Parent SHA1</th>
              <th>Bug File Path</th>
              <th>Fix Patch</th>
              <th>Project Name</th>
              <th>Bug Line Num</th>
              <th>Bug Node Start Char</th>
              <th>Bug Node Length</th>
              <th>Fix Line Num</th>
              <th>Fix Node Start Char</th>
              <th>Fix Node Length</th>
              <th>Source Before Fix</th>
              <th>Source After Fix</th>
            </tr>
          </thead>
          <tbody>
            <tr :key="i" v-for="(entry, i) in filteredEntries">
              <td>{{ entry.fixCommitSHA1 }}</td>
              <td>{{ entry.fixCommitParentSHA1 }}</td>
              <td class="text-left" :title="entry.bugFilePath">
                {{ entry.bugFilePath.slice(0, 30) }}
              </td>
              <td class="text-left" :title="entry.fixPatch">
                <code>{{ entry.fixPatch.slice(0, 30) }}</code>
              </td>
              <td>{{ entry.projectName }}</td>
              <td>{{ entry.bugLineNum }}</td>
              <td>{{ entry.bugNodeStartChar }}</td>
              <td>{{ entry.bugNodeLength }}</td>
              <td>{{ entry.fixLineNum }}</td>
              <td>{{ entry.fixNodeStartChar }}</td>
              <td>{{ entry.fixNodeLength }}</td>
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
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Vue from "vue";
import stubs from "@/../../dataset/sstubs.json";

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
}

export default Vue.extend({
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
      entries: stubs as SStuBs[],
      filteredEntries: [] as SStuBs[],
      expanded: [] as { bugFilePath: boolean; fixPatch: boolean }[]
    };
  },
  methods: {
    filterEntries: function() {
      const filteredEntries = this.entries.filter(entry => {
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

      this.filteredEntries = filteredEntries.slice(0, 50);
      this.expanded = filteredEntries.map(() => {
        return {
          bugFilePath: false,
          fixPatch: false
        };
      });
    }
  }
});
</script>
