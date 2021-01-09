import {Category} from './Category';

export class Item {
  id: number;
  name: string;
  description: string;
  specifications: string;
  price: number;
  brand: string;
  quantity: number;
  insertDate: Date;
  category: Category;
  discount: number;
  picture: string;
  sellMoney: number;

  finalPrice(): number {
    if (this.discount !== 0) {
      return (this.quantity * (this.price * (1 - this.discount / 100)));
    }
    return 0;
  }
}
