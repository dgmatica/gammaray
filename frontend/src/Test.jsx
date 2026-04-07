import { useState } from "react"

export default function Test() {
  const [count, setCount] = useState(0)
  const [count1, setCount1] = useState(1)
  return (
    <>
      <button onClick={() => setCount(count + 1)}>
        This button is +1: {count}
      </button>

      <button onClick={() => setCount1(count * 2)}>
        This button is *2: {count1}
      </button>
    </>
  )


}
