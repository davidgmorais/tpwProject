import { Cart } from './Cart';
import { Item } from './Item';

export class OrderItem {
  id: number;
  item: Item;
  cart: Cart;
  qty: number;
}
