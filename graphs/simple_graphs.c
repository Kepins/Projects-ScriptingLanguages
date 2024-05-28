#include <Python.h>
#include <structmember.h>

typedef struct Node Node;

struct Node{
    uint16_t edge;
    Node* next;
    Node* prev;
};


// Define the IncidenceMatrix structure
typedef struct {
    PyObject_HEAD;
    uint16_t vertices;
    Node* head;
} IncidenceMatrix;

// Method declarations
static int IncidenceMatrix_init(IncidenceMatrix *self, PyObject *args, PyObject *kwds);
static void IncidenceMatrix_dealloc(IncidenceMatrix *self);

// Standard methods
static PyObject* IncidenceMatrix_number_of_vertices(IncidenceMatrix *self);
static PyObject* IncidenceMatrix_vertices(IncidenceMatrix *self);
static PyObject* IncidenceMatrix_vertex_degree(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_vertex_neighbors(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_add_vertex(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_delete_vertex(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_number_of_edges(IncidenceMatrix *self);
static PyObject* IncidenceMatrix_edges(IncidenceMatrix *self);
static PyObject* IncidenceMatrix_is_edge(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_add_edge(IncidenceMatrix *self, PyObject *args);
static PyObject* IncidenceMatrix_delete_edge(IncidenceMatrix *self, PyObject *args);

// Comparasion methods
//static PyObject* IncidenceMatrix_richcompare(PyObject *self, PyObject *other, int op);

// Chosen method
static PyObject* IncidenceMatrix_create_complete_bipartite(PyObject *cls, PyObject *args);

// Define the methods of the class
static PyMethodDef IncidenceMatrix_methods[] = {
    {"number_of_vertices", (PyCFunction) IncidenceMatrix_number_of_vertices, METH_NOARGS, "Zwraca liczbę wierzchołków grafu."},
    {"vertices", (PyCFunction) IncidenceMatrix_vertices, METH_NOARGS, "Zwraca zbiór wierzchołków grafu."},
    {"vertex_degree", (PyCFunction) IncidenceMatrix_vertex_degree, METH_VARARGS, "Zwraca stopień wierzchołka."},
    {"vertex_neighbors", (PyCFunction) IncidenceMatrix_vertex_neighbors, METH_VARARGS, "Zwraca sąsiedztwo podanego wierzchołka."},
    {"add_vertex", (PyCFunction) IncidenceMatrix_add_vertex, METH_VARARGS, "Dodaje do grafu podany wierzchołek."},
    {"delete_vertex", (PyCFunction) IncidenceMatrix_delete_vertex, METH_VARARGS, "Usuwa z grafu podany wierzchołek i wszystkie incydentne z nim krawędzie."},
    {"number_of_edges", (PyCFunction) IncidenceMatrix_number_of_edges, METH_NOARGS, "Zwraca liczbę krawędzi grafu."},
    {"edges", (PyCFunction) IncidenceMatrix_edges, METH_NOARGS, "Zwraca zbiór krawędzi grafu."},
    {"is_edge", (PyCFunction) IncidenceMatrix_is_edge, METH_VARARGS, "Zwraca informację o tym, czy podane wierzchołki z sobą sąsiadują."},
    {"add_edge", (PyCFunction) IncidenceMatrix_add_edge, METH_VARARGS, "Dodaje do grafu podaną krawędź."},
    {"delete_edge", (PyCFunction) IncidenceMatrix_delete_edge, METH_VARARGS, "Usuwa z grafu podaną krawędź."},
    {"create_complete_bipartite", (PyCFunction) IncidenceMatrix_create_complete_bipartite, METH_VARARGS | METH_STATIC, "Zwraca graf dwudzielny pełny Kn,m."},
    {NULL}  /* Sentinel */
};

// Define the type object for IncidenceMatrix
static PyTypeObject IncidenceMatrixType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "simple_graphs.IncidenceMatrix",
    .tp_doc = "simple_graphs.IncidenceMatrix",
    .tp_basicsize = sizeof(IncidenceMatrix),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) IncidenceMatrix_init,
    .tp_dealloc = (destructor) IncidenceMatrix_dealloc,
    .tp_methods = IncidenceMatrix_methods,
    //.tp_richcompare = (richcmpfunc)IncidenceMatrix_richcompare,
};

// Define the module methods
static PyMethodDef module_methods[] = {
    {NULL}  /* Sentinel */
};

// Define the module
static struct PyModuleDef incidencematrixmodule = {
    PyModuleDef_HEAD_INIT,
    "simple_graphs",
    "simple_graphs module",
    -1,
    module_methods
};

// Module initialization function
PyMODINIT_FUNC PyInit_simple_graphs(void) {
    PyObject *m;
    if (PyType_Ready(&IncidenceMatrixType) < 0)
        return NULL;

    m = PyModule_Create(&incidencematrixmodule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&IncidenceMatrixType);
    PyModule_AddObject(m, "IncidenceMatrix", (PyObject *) &IncidenceMatrixType);
    return m;
}

// Method implementations
static int IncidenceMatrix_init(IncidenceMatrix *self, PyObject *args, PyObject *kwds) {
    self->vertices = 0;
    self->head = NULL;

    const char *default_text = "?";
    char *text = (char *)default_text;

    if (!PyArg_ParseTuple(args, "|s", &text)) {
        return -1; // Return -1 if argument parsing fails
    }

    int n = text[0] - 63;
    self->vertices = (1U << n) - 1;

    int x_bits = n*(n-1)/2;
    int x_bytes = x_bits / 6;
    if (x_bits % 6 !=0){
        x_bytes++;
    }
    int x_bit = 0;
    for(int i=1; i<n;i++){
        for(int j=0; j<i;j++){
            int text_byte = x_bit/6 + 1;
            int text_bit = 5 - x_bit % 6;

            char byte = text[text_byte] - 63;
            if(byte & (1U << text_bit)){
                // Allocate memory for a new Node
                Node* new_node = (Node*)malloc(sizeof(Node));
                if (new_node == NULL) {
                    PyErr_NoMemory(); // Set a memory allocation error
                    return -1;      // Return -1 to indicate failure
                }

                // Initialize the new Node
                new_node->edge = (1U << i) | (1U << j);
                new_node->next = NULL;
                new_node->prev = NULL;

                // Insert the new node at the head of the linked list
                if (self->head != NULL) {
                    self->head->prev = new_node;
                    new_node->next = self->head;
                }
                self->head = new_node;
            }
            x_bit ++;
        }
    }
    return 0;
}

static void IncidenceMatrix_dealloc(IncidenceMatrix *self) {
    Node* current = self->head;
    while (current != NULL) {
        Node* to_free = current;
        current = current->next;
        free(to_free);
    }

    Py_TYPE(self)->tp_free((PyObject *) self);
}

static PyObject* IncidenceMatrix_number_of_vertices(IncidenceMatrix *self) {
    return PyLong_FromLong(__builtin_popcount(self->vertices));
}

static PyObject* IncidenceMatrix_vertices(IncidenceMatrix *self) {
    // Create a new Python set object
    PyObject *set = PySet_New(NULL);
    if (!set) {
        return NULL; // Set creation failed
    }

    uint16_t vertices = self->vertices; 
    while (vertices) {
        PyObject *vert = PyLong_FromLong(__builtin_ctz(vertices));
        if (!vert) {
            Py_DECREF(set); // Decrease reference count of set
            return NULL;    // Integer creation failed
        }

        if (PySet_Add(set, vert) < 0) {
            Py_DECREF(vert); // Decrease reference count of num
            Py_DECREF(set); // Decrease reference count of set
            return NULL;    // Adding to set failed
        }

        Py_DECREF(vert); // Decrease reference count of num

        vertices &= vertices - 1;  // Remove the lowest set bit
    }

    // Return the set
    return set;
}

static PyObject* IncidenceMatrix_vertex_degree(IncidenceMatrix *self, PyObject *args) {
    int in_vertex;
    
    // Parse the input arguments to get two int values
    if (!PyArg_ParseTuple(args, "i", &in_vertex)) {
        return NULL; // Return NULL if argument parsing fails
    }
    int vertex_degree = 0;
    Node* current = self->head;
    while (current != NULL) {
        int edge = current->edge;
        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        if(in_vertex == vertex1 || in_vertex == vertex2){
            vertex_degree++;
        }

        current = current->next;
    }
    return PyLong_FromLong(vertex_degree);
}

static PyObject* IncidenceMatrix_vertex_neighbors(IncidenceMatrix *self, PyObject *args) {
    int in_vertex;
    
    // Parse the input arguments to get two int values
    if (!PyArg_ParseTuple(args, "i", &in_vertex)) {
        return NULL; // Return NULL if argument parsing fails
    }

    // Create a new Python set object
    PyObject *set = PySet_New(NULL);
    if (!set) {
        return NULL; // Set creation failed
    }

    Node* current = self->head;
    while (current != NULL) {
        int edge = current->edge;
        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        if(in_vertex == vertex1 || in_vertex == vertex2){
            PyObject *num = NULL;
            if (in_vertex == vertex1){
                num = PyLong_FromLong(vertex2);
            }
            else {
                num = PyLong_FromLong(vertex1);
            }
            if (!num) {
                Py_DECREF(set); // Decrease reference count of set
                return NULL;    // Integer creation failed
            }
            if (PySet_Add(set, num) < 0) {
                Py_DECREF(num); // Decrease reference count of num
                Py_DECREF(set); // Decrease reference count of set
                return NULL;    // Adding to set failed
            }
            Py_DECREF(num); // Decrease reference count of num
        }
        current = current->next;
    }
    return set;
}

static PyObject* IncidenceMatrix_add_vertex(IncidenceMatrix *self, PyObject *args) {
    int vertex_idx;
    if (!PyArg_ParseTuple(args, "i", &vertex_idx)) {
        return NULL;
    }
    self->vertices |= 1U << vertex_idx;
    Py_RETURN_NONE;
}

static PyObject* IncidenceMatrix_delete_vertex(IncidenceMatrix *self, PyObject *args) {
    int vertex_idx;
    if (!PyArg_ParseTuple(args, "i", &vertex_idx)) {
        return NULL;
    }
    self->vertices &= ~(1U << vertex_idx);

    // Remove all edges associated with vertex_idx
    Node* current = self->head;
    while (current != NULL) {
        int edge = current->edge;
        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        Node* check_delete = current;
        current = current->next;

        if(vertex_idx == vertex1 || vertex_idx == vertex2){
            if(check_delete == self->head && check_delete->next == NULL){
                self->head = NULL;
            }
            else if(check_delete == self->head){
                check_delete->next->prev = NULL;
                self->head = check_delete->next;
            }
            else if(check_delete->next == NULL){
                check_delete->prev->next = NULL;
            }
            else{
                check_delete->prev->next = check_delete->next;
                check_delete->next->prev = check_delete->prev;
            }
            free(check_delete);
        }
    }

    Py_RETURN_NONE;
}

static PyObject* IncidenceMatrix_number_of_edges(IncidenceMatrix *self) {
    int number_of_edges = 0;
    Node* current = self->head;
    while (current != NULL) {
        number_of_edges++;
        current = current->next;
    }
    return PyLong_FromLong(number_of_edges);
}

static PyObject* IncidenceMatrix_edges(IncidenceMatrix *self) {
    // Create a new Python set object
    PyObject *set = PySet_New(NULL);
    if (!set) {
        return NULL; // Set creation failed
    }

    Node* current = self->head;
    while (current != NULL) {
        int edge = current->edge;
        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        PyObject* edge_tuple = PyTuple_Pack(2, PyLong_FromLong(vertex1), PyLong_FromLong(vertex2));
        if (edge_tuple == NULL) {
            Py_DECREF(set); // Clean up on error
            return NULL;
        }

        if (PySet_Add(set, edge_tuple) < 0) {
            Py_DECREF(edge_tuple);
            Py_DECREF(set);
            return NULL;
        }

        Py_DECREF(edge_tuple); // Decrement reference count after adding to the list
        current = current->next;
    }

    return set;
}

static PyObject* IncidenceMatrix_is_edge(IncidenceMatrix *self, PyObject *args) {
    int in_vertex_1;
    int in_vertex_2;
    
    // Parse the input arguments to get two int values
    if (!PyArg_ParseTuple(args, "ii", &in_vertex_1, &in_vertex_2)) {
        return NULL; // Return NULL if argument parsing fails
    }
    
    if(in_vertex_1 > in_vertex_2){
        // SWAP
        in_vertex_1 = in_vertex_1 ^ in_vertex_2;
        in_vertex_2 = in_vertex_1 ^ in_vertex_2;
        in_vertex_1 = in_vertex_1 ^ in_vertex_2;
    }

    Node* current = self->head;
    while (current != NULL) {
        int edge = current->edge;
        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        if(in_vertex_1 == vertex1 && in_vertex_2 == vertex2){
            Py_RETURN_TRUE;
        }

        current = current->next;
    }
    Py_RETURN_FALSE;
}

static PyObject* IncidenceMatrix_add_edge(IncidenceMatrix *self, PyObject *args) {
    int vertex_1;
    int vertex_2;
    
    // Parse the input arguments to get two int values
    if (!PyArg_ParseTuple(args, "ii", &vertex_1, &vertex_2)) {
        return NULL; // Return NULL if argument parsing fails
    }

    // Allocate memory for a new Node
    Node* new_node = (Node*)malloc(sizeof(Node));
    if (new_node == NULL) {
        PyErr_NoMemory(); // Set a memory allocation error
        return NULL;      // Return NULL to indicate failure
    }

    // Initialize the new Node
    new_node->edge = (1U << vertex_1) | (1U << vertex_2);
    new_node->next = NULL;
    new_node->prev = NULL;

    // Insert the new node at the head of the linked list
    if (self->head != NULL) {
        self->head->prev = new_node;
        new_node->next = self->head;
    }
    self->head = new_node;

    Py_RETURN_NONE;
}

static PyObject* IncidenceMatrix_delete_edge(IncidenceMatrix *self, PyObject *args) {
    int in_vertex_1;
    int in_vertex_2;
    
    // Parse the input arguments to get two int values
    if (!PyArg_ParseTuple(args, "ii", &in_vertex_1, &in_vertex_2)) {
        return NULL; // Return NULL if argument parsing fails
    }
    
    if(in_vertex_1 > in_vertex_2){
        // SWAP
        in_vertex_1 = in_vertex_1 ^ in_vertex_2;
        in_vertex_2 = in_vertex_1 ^ in_vertex_2;
        in_vertex_1 = in_vertex_1 ^ in_vertex_2;
    }

    Node* current = self->head;
    while (current != NULL) {
        uint16_t edge = current->edge;

        int vertex1 = __builtin_ctz(edge); // Find index of the first set bit
        edge &= edge - 1; // Remove the first set bit
        int vertex2 = __builtin_ctz(edge); // Find index of the second set bit

        
        if(in_vertex_1 == vertex1 && in_vertex_2 == vertex2){
            if(current == self->head && current->next == NULL){
                self->head = NULL;
            }
            else if(current == self->head){
                current->next->prev = NULL;
                self->head = current->next;
            }
            else if(current->next == NULL){
                current->prev->next = NULL;
            }
            else{
                current->prev->next = current->next;
                current->next->prev = current->prev;
            }
            free(current);
            Py_RETURN_NONE;
        }

        current = current->next;
    }
    Py_RETURN_NONE;
}

static PyObject* IncidenceMatrix_create_complete_bipartite(PyObject *cls, PyObject *args) {
    int n;
    int m;

    // Parse the input argument to get the number of vertices
    if (!PyArg_ParseTuple(args, "ii", &n, &m)) {
        return NULL; // Return NULL if argument parsing fails
    }

    // Allocate memory for the IncidenceMatrix struct
    IncidenceMatrix *graph = (IncidenceMatrix *)PyObject_New(IncidenceMatrix, &IncidenceMatrixType);
    if (graph == NULL) {
        return NULL;
    }

    PyObject *init_args = PyTuple_New(0);
    if (!init_args) {
        Py_DECREF(graph);  // Clean up the created object
        return NULL;
    }

    int init_result = IncidenceMatrix_init(graph, init_args, NULL);
    Py_DECREF(init_args);  // Decrease reference count of args

    if (init_result != 0) {
        Py_DECREF(graph);  // Clean up the created object
        return NULL;
    }

    // Init vertices
    graph->vertices = (1U << (n+m)) - 1;

    for(int i=0;i<n;i++){
        for(int j=n;j<n+m;j++){
            // Allocate memory for a new Node
            Node* new_node = (Node*)malloc(sizeof(Node));
            if (new_node == NULL) {
                PyErr_NoMemory(); // Set a memory allocation error
                return NULL;      // Return NULL to indicate failure
            }

            new_node->edge = (1U << i) | (1U << j);
            new_node->next = NULL;
            new_node->prev = NULL;

            // Insert the new node at the head of the linked list
            if (graph->head != NULL) {
                graph->head->prev = new_node;
                new_node->next = graph->head;
            }
            graph->head = new_node;
        }
    }

    return (PyObject *)graph;
}