<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <!-- <h1>Keyence monitor</h1> -->
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <div class="col-lg-6">
          <div class="input-group">
            <input v-model="commit" class="form-control" placeholder="注釋">
            <input v-model="addr" class="form-control" placeholder="暫存器名稱">
            <span class="input-group-btn">
              <button class="btn btn-secondary"
              type="button" @click="onSubmit(addr)">新增暫存器</button>
            </span>
          </div>
        </div>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">注釋</th>
              <th scope="col">暫存器</th>
              <th scope="col">狀態</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(addr, index) in addrs" :key="index"
            :class="[{ 'bg-success': addr.bool , 'bg-info':addr.str }, errorClass]">
              <td>{{ addr.commit }}</td>
              <td>{{ addr.title }}</td>
              <td>
                <span v-if="addr.bool" >Yes</span>
                <span v-else-if="addr.str" >{{addr.myvalue}}</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.addr-update-modal
                    @click="editAddr(addr)">
                    Update
                </button>
                <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteAddr(addr)">
                    Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- <b-modal ref="addAddrModal"
          id="addr-modal"
          title="Add a new addr"
          hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                  label="Title:"
                  label-for="form-title-input">
        <b-form-input id="form-title-input"
                      type="text"
                      v-model="addAddrForm.title"
                      required
                      placeholder="Enter title">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-myvalue-group"
                    label="myvalue:"
                    label-for="form-myvalue-input">
          <b-form-input id="form-myvalue-input"
                        type="text"
                        v-model="addAddrForm.myvalue"
                        required
                        placeholder="Enter myvalue">
          </b-form-input>
        </b-form-group>
      <b-form-group id="form-bool-group">
        <b-form-checkbox-group v-model="addAddrForm.bool" id="form-checks">
          <b-form-checkbox myvalue="true">bool?</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-modal> -->
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
      <b-button type="submit" variant="primary">Update</b-button>
      <b-button type="reset" variant="danger">Cancel</b-button>
    </b-form>
  </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      addrs: [],
      addAddrForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
        commit: '',
      },
      editForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
        commit: '',
      },
      message: '',
      errorClass: 'bg-primary',
    };
  },
  components: {
    alert: Alert,
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
          this.message = 'addr added!';
          this.showMessage = true;
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
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.myvalue = '';
      this.editForm.bool = [];
      this.editForm.str = [];
      this.editForm.commit = '';
    },
    onSubmit(addr) {
      // this.$refs.addAddrModal.hide();
      let bool = false;
      if (this.addAddrForm.bool[0]) bool = true;
      const payload = {
        title: addr,
        bool, // property shorthand
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
      };
      this.updateAddr(payload, this.editForm.id);
    },
    updateAddr(payload, addrID) {
      const path = `http://localhost:5000/addrs/${addrID}`;
      axios.put(path, payload)
        .then(() => {
          this.getAddrs();
          this.message = 'Addr updated!';
          this.showMessage = true;
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
      this.getAddrs(); // why?
    },
    removeAddr(addrID) {
      const path = `http://localhost:5000/addrs/${addrID}`;
      axios.delete(path)
        .then(() => {
          this.getAddrs();
          this.message = 'Addr removed!';
          this.showMessage = true;
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
  },
  created() {
    this.getAddrs();
    this.timer = setInterval(this.getAddrs, 1000);
    clearInterval(this.timer);
  },
};
</script>
