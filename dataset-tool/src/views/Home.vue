
<template>
  <div class="home">
    <div class="col-3">
      <input type="text" class="form-control" v-model="fixCommitSHA1">
      <input type="text" class="form-control" v-model="fixCommitParentSHA1">
      <input type="text" class="form-control" v-model="bugFilePath">
      <input type="text" class="form-control" v-model="fixPatch">
      <input type="text" class="form-control" v-model="projectName">
      <input type="text" class="form-control" v-model="bugLineNum">
      <input type="text" class="form-control" v-model="bugNodeStartChar">
      <input type="text" class="form-control" v-model="bugNodeLength">
      <input type="text" class="form-control" v-model="fixLineNum">
      <input type="text" class="form-control" v-model="fixNodeStartChar">
      <input type="text" class="form-control" v-model="fixNodeLength">
      <input type="text" class="form-control" v-model="sourceBeforeFix">
      <input type="text" class="form-control" v-model="sourceAfterFix">
      <button @click="filterEntries">Search</button>
    </div>
    <div class="col-12">
      <table class="table">
        <thead><tr>
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
        </tr></thead>
        <tbody>
        <tr :key="i" v-for="(entry,i) in filteredEntries">
          <td>{{entry.fixCommitSHA1}}</td>
          <td>{{entry.fixCommitParentSHA1}}</td>
          <td class="text-left" :title="entry.bugFilePath">{{entry.bugFilePath.slice(0,30)}}</td>
          <td class="text-left" :title="entry.fixPatch">{{entry.fixPatch.slice(0,30)}}</td>
          <td>{{entry.projectName}}</td>
          <td>{{entry.bugLineNum}}</td>
          <td>{{entry.bugNodeStartChar}}</td>
          <td>{{entry.bugNodeLength}}</td>
          <td>{{entry.fixLineNum}}</td>
          <td>{{entry.fixNodeStartChar}}</td>
          <td>{{entry.fixNodeLength}}</td>
          <td>{{entry.sourceBeforeFix}}</td>
          <td>{{entry.sourceAfterFix}}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script lang="ts">
import {Component, Vue} from "vue-property-decorator";
import HelloWorld from "@/components/HelloWorld.vue"; // @ is an alias to /src
import stubs from '../dataset/sstubs.json'

@Component({
  components: {
    HelloWorld
  },
  data() {
    return {
      fixCommitSHA1:'',
      fixCommitParentSHA1:'' ,
      bugFilePath: '',
      fixPatch:'',
      projectName:'',
      bugLineNum:'',
      bugNodeStartChar:'',
      bugNodeLength:'',
      fixLineNum:'',
      fixNodeStartChar:'',
      fixNodeLength:'',
      sourceBeforeFix:'',
      sourceAfterFix:'',
      entries: stubs,
      filteredEntries: [],
      expanded:[]
    }
  },
  methods:
      {
        filterEntries: function (){
          const filteredEntries = this.entries.filter((entry)=>{
            return entry.fixCommitSHA1.includes(this.fixCommitSHA1)
            && entry.fixCommitParentSHA1.includes(this.fixCommitParentSHA1)
            && entry.bugFilePath.includes(this.bugFilePath)
            && entry.fixPatch.includes(this.fixPatch)
            && entry.projectName.includes(this.projectName)
            && entry.bugLineNum.includes(this.bugLineNum)
            && entry.bugNodeStartChar.includes(this.bugNodeStartChar)
            && entry.bugNodeLength.includes(this.bugNodeLength)
            && entry.fixLineNum.includes(this.fixLineNum)
            && entry.fixNodeLength.includes(this.fixNodeLength)
            && entry.sourceBeforeFix.includes(this.sourceBeforeFix)
            && entry.sourceAfterFix.includes(this.sourceAfterFix);
          });
          this.filteredEntries = filteredEntries;
          this.expanded = filteredEntries.map(()=>{
            return {
              bugFilePath:false,
              fixPatch:false
            }
          })
        }
      }
})
export default class Home extends Vue {
}
</script>
