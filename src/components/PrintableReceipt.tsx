import { forwardRef } from "react";

interface ReceiptProps {
  sale: {
    id: string;
    date: string;
    customer: string;
    items: Array<{
      productName: string;
      quantity: number;
      price: number;
    }>;
    subtotal: number;
    discount: number;
    total: number;
    paymentMethod: string;
  };
}

export const PrintableReceipt = forwardRef<HTMLDivElement, ReceiptProps>(
  ({ sale }, ref) => {
    return (
      <div ref={ref} className="hidden print:block print:p-8">
        <div className="max-w-md mx-auto">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold">SHoSHoP</h1>
            <p className="text-sm text-gray-600">Sales Receipt</p>
          </div>

          <div className="mb-4 pb-4 border-b border-gray-300">
            <div className="flex justify-between text-sm">
              <span>Receipt #:</span>
              <span className="font-semibold">{sale.id}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Date:</span>
              <span>{sale.date}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span>Customer:</span>
              <span>{sale.customer}</span>
            </div>
          </div>

          <div className="mb-4">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-300">
                  <th className="text-left py-2">Item</th>
                  <th className="text-center py-2">Qty</th>
                  <th className="text-right py-2">Price</th>
                  <th className="text-right py-2">Total</th>
                </tr>
              </thead>
              <tbody>
                {sale.items.map((item, idx) => (
                  <tr key={idx} className="border-b border-gray-200">
                    <td className="py-2">{item.productName}</td>
                    <td className="text-center">{item.quantity}</td>
                    <td className="text-right">{item.price.toLocaleString()}</td>
                    <td className="text-right">
                      {(item.price * item.quantity).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="space-y-2 mb-4 pb-4 border-b border-gray-300">
            <div className="flex justify-between text-sm">
              <span>Subtotal:</span>
              <span>{sale.subtotal.toLocaleString()} ETB</span>
            </div>
            {sale.discount > 0 && (
              <div className="flex justify-between text-sm">
                <span>Discount:</span>
                <span>-{sale.discount.toLocaleString()} ETB</span>
              </div>
            )}
            <div className="flex justify-between text-lg font-bold">
              <span>Total:</span>
              <span>{sale.total.toLocaleString()} ETB</span>
            </div>
          </div>

          <div className="text-sm mb-4">
            <div className="flex justify-between">
              <span>Payment Method:</span>
              <span className="font-semibold">{sale.paymentMethod}</span>
            </div>
          </div>

          <div className="text-center text-xs text-gray-600 mt-6">
            <p>Thank you for Shopping With Us!</p>
            <p className="mt-1">SHoSHoP.com</p>
          </div>
        </div>
      </div>
    );
  }
);

PrintableReceipt.displayName = "PrintableReceipt";
