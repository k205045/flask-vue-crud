<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Keyence monitor</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <div class="col-lg-6">
          <div class="input-group">
            <input v-model="addr" class="form-control" placeholder="Ex:B01">
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
              <th scope="col">暫存器</th>
              <th scope="col">狀態</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(book, index) in books" :key="index"
            :class="[{ 'bg-success': book.bool , 'bg-info':book.str }, errorClass]">
              <td>{{ book.title }}</td>
              <!-- <td>{{ book.myvalue }}</td> -->
              <td>
                <span v-if="book.bool" >Yes</span>
                <span v-else-if="book.str" >{{book.myvalue}}</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                    type="button"
                    class="btn btn-warning btn-sm"
                    v-b-modal.book-update-modal
                    @click="editBook(book)">
                    Update
                </button>
                <button
                    type="button"
                    class="btn btn-danger btn-sm"
                    @click="onDeleteBook(book)">
                    Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <!-- <b-modal ref="addBookModal"
          id="book-modal"
          title="Add a new book"
          hide-footer>
    <b-form @submit="onSubmit" @reset="onReset" class="w-100">
    <b-form-group id="form-title-group"
                  label="Title:"
                  label-for="form-title-input">
        <b-form-input id="form-title-input"
                      type="text"
                      v-model="addBookForm.title"
                      required
                      placeholder="Enter title">
        </b-form-input>
      </b-form-group>
      <b-form-group id="form-myvalue-group"
                    label="myvalue:"
                    label-for="form-myvalue-input">
          <b-form-input id="form-myvalue-input"
                        type="text"
                        v-model="addBookForm.myvalue"
                        required
                        placeholder="Enter myvalue">
          </b-form-input>
        </b-form-group>
      <b-form-group id="form-bool-group">
        <b-form-checkbox-group v-model="addBookForm.bool" id="form-checks">
          <b-form-checkbox myvalue="true">bool?</b-form-checkbox>
        </b-form-checkbox-group>
      </b-form-group>
      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </b-modal> -->
  <b-modal ref="editBookModal"
          id="book-update-modal"
          title="Update"
          hide-footer>
    <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
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
      books: [],
      addBookForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
      },
      editForm: {
        title: '',
        bool: [],
        str: [],
        myvalue: '',
      },
      message: '',
      errorClass: 'bg-primary',
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getBooks() {
      const path = 'http://localhost:5000/books';
      axios.get(path)
        .then((res) => {
          this.books = res.data.books;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addBook(payload) {
      const path = 'http://localhost:5000/books';
      axios.post(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'addr added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.log(error);
          this.getBooks();
        });
    },
    initForm() {
      this.addBookForm.title = '';
      this.addBookForm.myvalue = '';
      this.addBookForm.bool = [];
      this.addBookForm.str = [];
      this.editForm.id = '';
      this.editForm.title = '';
      this.editForm.myvalue = '';
      this.editForm.bool = [];
      this.editForm.str = [];
    },
    onSubmit(addr) {
      // this.$refs.addBookModal.hide();
      let bool = false;
      if (this.addBookForm.bool[0]) bool = true;
      const payload = {
        title: addr,
        bool, // property shorthand
      };
      this.addBook(payload);
      this.initForm();
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addBookModal.hide();
      this.initForm();
    },
    editBook(book) {
      this.editForm = book;
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      const payload = {
        title: this.editForm.title,
        bool: this.editForm.bool,
        str: this.editForm.str,
        myvalue: this.editForm.myvalue,
      }
      this.updateBook(payload ,this.editForm.id);
    },
    updateBook(payload, bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.put(path, payload)
        .then(() => {
          this.getBooks();
          this.message = 'Book updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editBookModal.hide();
      this.initForm();
      this.getBooks(); // why?
    },
    removeBook(bookID) {
      const path = `http://localhost:5000/books/${bookID}`;
      axios.delete(path)
        .then(() => {
          this.getBooks();
          this.message = 'Book removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getBooks();
        });
    },
    onDeleteBook(book) {
      this.removeBook(book.id);
    },
    checkclass(book) {
      this.removeBook(book.id);
    },
  },
  created() {
    this.getBooks();
    this.timer = setInterval(this.getBooks, 1000);
    clearInterval(this.timer);
  },
};
</script>
