#include <cstring>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
// #include <stdexcept>

#include <boost/interprocess/ipc/message_queue.hpp>
#include <boost/python.hpp>

using namespace boost::interprocess;

struct Item {
  char ticker[20];
  char maybe_investor[1000];
  char external[1000];
  char last_time_str[200];
};

// https://www.boost.org/doc/libs/1_37_0/libs/python/doc/v2/manage_new_object.html
struct Foo {
  void *x;
};

Foo *create(std::string name, int max) {
  // Erase previous message queue
  message_queue::remove(name.c_str());

  // Create a message_queue.
  message_queue *mq = new message_queue(create_only // only create
                                        ,
                                        name.c_str(),
                                        max // max message number
                                        ,
                                        2220 // sizeof(int) // max message size
  );

  auto tmp = new Foo();
  tmp->x = mq;
  return tmp;
}

Foo *open_queue(std::string name) {
  try {
    message_queue *mq = new message_queue(open_only // only open
                                          ,
                                          name.c_str());
    auto tmp = new Foo();
    tmp->x = mq;
    return tmp;
  } catch (interprocess_exception &ex) {
    message_queue::remove("message_queue");
    std::cout << ex.what() << std::endl;
    return 0;
  }
}

std::string send(Foo *tmp, std::string ticker, std::string maybe_investor,
                 std::string external, std::string last_time_str) {
  Item i;
  strcpy(i.ticker, ticker.c_str());
  strcpy(i.maybe_investor, maybe_investor.c_str());
  strcpy(i.external, external.c_str());
  strcpy(i.last_time_str, last_time_str.c_str());

  message_queue *mq = (message_queue *)tmp->x;
  mq->send(&i, sizeof(i), 0);

  return "ok";
}

boost::python::tuple receive(Foo *tmp){
    // clang-format off
  BOOST_TRY {
    message_queue *mq = (message_queue *)tmp->x;

    unsigned int priority;
    message_queue::size_type recvd_size;

    Item *i = new Item();
    mq->receive(i, sizeof(Item), recvd_size, priority);
    return boost::python::make_tuple(std::string(i->ticker), std::string(i->maybe_investor), 
                                  std::string(i->external),
                                  std::string(i->last_time_str));
  }
  BOOST_CATCH(interprocess_exception &ex) {
    std::cout << ex.what() << std::endl;
    //return 0;
  }
  BOOST_CATCH_END
}

boost::python::tuple try_receive(Foo *tmp) {
  try {
    message_queue *mq = (message_queue *)tmp->x;

    unsigned int priority;
    message_queue::size_type recvd_size;

    Item *i = new Item();
    bool got = mq->try_receive(i, sizeof(Item), recvd_size, priority);
    if (!got) {
      // would block
      return boost::python::make_tuple(std::string("would"));
    }
    return boost::python::make_tuple(std::string(i->ticker), std::string(i->maybe_investor), 
                                  std::string(i->external),
                                  std::string(i->last_time_str));
  }
  catch(interprocess_exception &ex) {
    std::cout << ex.what() << std::endl;
  }
}

int remove_queue(std::string name) {
  message_queue::remove(name.c_str());
  return 0;
}

BOOST_PYTHON_MODULE(_mq_sa) {
  using namespace boost::python;

  def("create", create, return_value_policy<manage_new_object>());
  // otherwise - No Python class registered for C++ class Foo
  class_<Foo>("Foo") /*.def("get_x", &Foo::get_x)*/;

  def("open", open_queue, args("name"), return_value_policy<manage_new_object>());

  def("send", send,
      args("ticker", "maybe_investor", "external", "last_time_str"),
      "send's docstring");

  def("receive", receive);
  class_<Item>("Item");

  def("remove", remove_queue);

  def("try_receive", try_receive);
}
