import React from "react";

const TextInput = ({
  placeholder,
  className,
  name,
  onChange,
  value,
}) => {

  return (
    <div style={{width: "100%"}}>
      <input
        className={`box-border w-full px-3 radius-md border-2 outline-none rounded-md py-2 ${className}`}
        spellCheck="false"
        placeholder={placeholder}
        onChange={onChange}
        value={value}
        />
      </div>
  );
};

export default TextInput;
