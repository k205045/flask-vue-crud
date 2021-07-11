<template>
  <div class="container-fluid">
    <div class="mt-3">
      <b-button-group>
        <b-button type="button" @click="timerON()" variant="success">開啟掃描</b-button>
        <b-button type="button" @click="timerOFF()" variant="info">關閉掃描</b-button>
      </b-button-group>
    </div>
    <br>
    <alert :message=message v-if="showMessage"></alert>
    <div class="row">
      <div class="col-6">
        <h2>Only Read</h2>
        <br>
        <div class="col-lg-6">
          <div class="input-group">
            <input v-model="commit1" class="form-control" placeholder="注釋">
            <input v-model="addr" class="form-control" placeholder="暫存器名稱">
            <span class="input-group-btn">
              <button class="btn btn-secondary"
              type="button" @click="onSubmit(addr, commit1, false)">新增暫存器</button>
            </span>
          </div>
        </div>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">注釋</th>
              <th scope="col">暫存器</th>
              <th scope="col">狀態</th>
              <th scope="col">位元</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <draggable v-model="addrs" tag="tbody" animation="500"
          chosen-class="chosen" @change=changeindex>
            <tr v-for="addr in addrs" :key="addr.id" v-show="!addr.ReadOrWrite"
            :class="[{ 'table-success': addr.bool , 'table-info':addr.str }, errorClass]">
              <td>{{ addr.commit }}</td>
              <td>{{ addr.title }}</td>
              <td>
                <span v-if="addr.bool" >Yes</span>
                <span v-else-if="addr.str" >{{addr.myvalue}}</span>
                <span v-else>No</span>
              </td>
              <td>
                {{ bcouponList[addr.selectnum].text }}
              </td>
              <td>
                <button
                    type="button"
                    class="btn table-warning btn-sm"
                    v-b-modal.addr-update-modal-2
                    @click="editAddr(addr)">
                    Update
                </button>
                <button
                    type="button"
                    class="btn table-danger btn-sm"
                    @click="onDeleteAddr(addr)">
                    Delete
                </button>
              </td>
            </tr>
          </draggable>
        </table>
      </div>
      <div class="col-6">
        <h2>Read and Write</h2>
        <br>
        <div class="col-lg-6">
          <div class="input-group">
            <input v-model="commit2" class="form-control" placeholder="注釋">
            <input v-model="addr2" class="form-control" placeholder="暫存器名稱">
            <span class="input-group-btn">
              <button class="btn btn-secondary"
              type="button" @click="onSubmit(addr2, commit2, true)">新增暫存器</button>
            </span>
          </div>
        </div>
        <br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">注釋</th>
              <th scope="col">暫存器</th>
              <th scope="col">狀態</th>
              <th scope="col">  位元</th>
              <th scope="col">操作</th>
            </tr>
          </thead>
          <draggable v-model="addrs" tag="tbody" animation="500"
          chosen-class="chosen" @change=changeindex>
            <tr v-for="addr in addrs" :key="addr.id" v-show="addr.ReadOrWrite"
            :class="[{ 'table-success': addr.bool , 'table-info':addr.str }, errorClass]">
              <td>{{ addr.commit }}</td>
              <td>{{ addr.title }}</td>
              <td>
                <span v-if="addr.bool" >Yes</span>
                <span v-else-if="addr.str" >{{addr.myvalue}}</span>
                <span v-else>No</span>
              </td>
              <td>
                {{ bcouponList[addr.selectnum].text }}
              </td>
              <td>
                <button
                    type="button"
                    class="btn table-warning btn-sm"
                    v-b-modal.addr-update-modal
                    @click="editAddr(addr)">
                    Update
                </button>
                <button
                    type="button"
                    class="btn table-danger btn-sm"
                    @click="onDeleteAddr(addr)">
                    Delete
                </button>
              </td>
            </tr>
          </draggable>
        </table>
      </div>
    </div>
    <b-modal ref="editAddrModal"
            id="addr-update-modal"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Commit:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.commit"
                        required
                        placeholder="Enter commit">
          </b-form-input>
        </b-form-group>
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group v-if="editForm.str" id="form-myvalue-edit-group"
                      label="myvalue:"
                      label-for="form-myvalue-edit-input">
            <b-form-input id="form-myvalue-edit-input"
                          type="text"
                          v-model="editForm.myvalue"
                          required
                          placeholder="Enter myvalue">
            </b-form-input>
          </b-form-group>
        <b-form-group v-if="!editForm.str" id="form-bool-edit-group">
          <b-form-checkbox-group v-model="editForm.bool" id="form-checks">
            <b-form-checkbox myvalue="true">status </b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                    label="bit:"
                    label-for="form-title-edit-select">
          <b-form-select v-model="editForm.selectnum"
            required
            :options="bcouponList"
            placeholder="Enter select">
          </b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editAddrModal"
            id="addr-update-modal-2"
            title="Update"
            hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-title-edit-group"
                    label="Commit:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.commit"
                        required
                        placeholder="Enter commit">
          </b-form-input>
        </b-form-group>
      <b-form-group id="form-title-edit-group"
                    label="Title:"
                    label-for="form-title-edit-input">
          <b-form-input id="form-title-edit-input"
                        type="text"
                        v-model="editForm.title"
                        required
                        placeholder="Enter title">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-title-edit-group"
                    label="bit:"
                    label-for="form-title-edit-select">
          <b-form-select v-model="editForm.selectnum"
            required
            :options="bcouponList"
            placeholder="Enter select">
          </b-form-select>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import 'vue-select/dist/vue-select.css';
import axios from 'axios';
import draggable from 'vuedraggable';
import Alert from '../../components/Alert';

export default {
  data() {
    return {
      bcouponList: [{
        value: '0',
        text: '布林',
      },
      {
        value: '1',
        text: '無符號16進位',
      },
      {
        value: '2',
        text: '有符號16進位',
      },
      {
        value: '3',
        text: '無符號32進位',
      },
      {
        value: '4',
        text: '有符號32進位',
      },
      ],
      bcouponSelected: '',
      addrs: [],
      addAddrForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
        commit: '',
        ReadOrWrite: [],
        selectnum: '',
      },
      editForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
        commit: '',
        ReadOrWrite: [],
        selectnum: '',
      },
      message: '',
      showMessage: false,
      errorClass: 'table-primary',
      drag: false,
    };
  },
  components: {
    alert: Alert,
    draggable,
  },
  methods: {
    getAddrs() {
      const path = 'http://localhost:5000/addrs';
      axios.get(path)
        .then((res) => {
          this.addrs = res.data.addrs;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addAddr(payload) {
      const path = 'http://localhost:5000/addrs';
      axios.post(path, payload)
        .then(() => {
          this.getAddrs();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getAddrs();
        });
    },
    initForm() {
      this.addAddrForm.title = '';
      this.addAddrForm.myvalue = '';
      this.addAddrForm.bool = [];
      this.addAddrForm.str = [];
      this.addAddrForm.commit = '';
      this.addAddrForm.selectnum = '0';
      this.addAddrForm.ReadOrWrite = [];
      this.editForm.title = '';
      this.editForm.myvalue = '';
      this.editForm.bool = [];
      this.editForm.str = [];
      this.editForm.commit = '';
      this.editForm.ReadOrWrite = [];
      this.editForm.selectnum = '0';
    },
    onSubmit(addr, commit1, read, bit) {
      // this.$refs.addAddrModal.hide();
      let bool = false;
      if (this.addAddrForm.bool[0]) bool = true;
      const payload = {
        commit: commit1,
        title: addr,
        bool, // property shorthand
        ReadOrWrite: read,
        selectnum: bit,
      };
      this.addAddr(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addAddrModal.hide();
      this.initForm();
    },
    editAddr(addr) {
      this.editForm = addr;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAddrModal.hide();
      const payload = {
        title: this.editForm.title,
        bool: this.editForm.bool,
        str: this.editForm.str,
        myvalue: this.editForm.myvalue,
        commit: this.editForm.commit,
        ReadOrWrite: this.editForm.ReadOrWrite,
        selectnum: this.editForm.selectnum,
      };
      this.updateAddr(payload, this.editForm.id);
    },
    updateAddr(payload, addrID) {
      const path = `http://localhost:5000/addrs/${addrID}`;
      axios.put(path, payload)
        .then(() => {
          this.getAddrs();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAddrs();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editAddrModal.hide();
      this.initForm();
      this.getAddrs();
    },
    removeAddr(addrID) {
      const path = `http://localhost:5000/addrs/${addrID}`;
      axios.delete(path)
        .then(() => {
          this.getAddrs();
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getAddrs();
        });
    },
    onDeleteAddr(addr) {
      this.removeAddr(addr.id);
    },
    checkclass(addr) {
      this.removeAddr(addr.id);
    },
    changeindex(evt) {
      const path = 'http://localhost:5000/change';
      axios.post(path, evt);
    },
    timerON() {
      this.timer = setInterval(this.getAddrs, 500);
      this.showMessage = false;
    },
    timerOFF() {
      clearInterval(this.timer);
      this.message = '停止刷新!';
      this.showMessage = true;
    },
  },
  created() {
    this.bcouponSelected = this.bcouponList[0];
    this.getAddrs();
    this.timer = setInterval(this.getAddrs, 500);
    // clearInterval(this.timer);
  },
};
</script>
